from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField
from datetime import datetime

class User(Document):
    name  = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    password = StringField(required=False)
    is_verified = BooleanField(default=False)
    otp = StringField()
    otp_expiry = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'users'}