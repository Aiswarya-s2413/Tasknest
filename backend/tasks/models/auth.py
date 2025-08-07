# models.py - Updated User model with Django authentication properties

from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField
from datetime import datetime

class User(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    password = StringField(required=False)
    is_verified = BooleanField(default=False)
    otp = StringField()
    otp_expiry = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'users'}

    # Add Django authentication properties
    @property
    def is_authenticated(self):
        """Always return True for authenticated users"""
        return True

    @property
    def is_anonymous(self):
        """Always return False for authenticated users"""
        return False

    @property
    def is_active(self):
        return self.is_verified

    @property
    def is_staff(self):
        return False

    def get_username(self):
        """Return email as username"""
        return self.email

    def __str__(self):
        return self.email

    def check_password(self, raw_password):
        """Check if the provided password is correct"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        """Set the user's password"""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    