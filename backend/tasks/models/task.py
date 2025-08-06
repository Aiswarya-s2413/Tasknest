from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    BooleanField,
    ReferenceField
)
from datetime import datetime
from tasks.models import User


class Task(Document):
    """
    Task model for managing user tasks
    """
    user = ReferenceField(User, required=True)  

    title = StringField(required=True, max_length=200)
    description = StringField()
    
    due_date = DateTimeField()  # For scheduling 
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    is_completed = BooleanField(default=False)
    completed_at = DateTimeField()

    # For scheduling tasks
    scheduled_time = DateTimeField()

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    priority = StringField(choices=PRIORITY_CHOICES, default='medium')

    meta = {
        'collection': 'tasks',
        'ordering': ['-created_at'],
        'indexes': ['title', 'due_date', 'is_completed']
    }

    def __str__(self):
        return f"{self.title} ({self.user.email})"

    def save(self, *args, **kwargs):
        """Override save to update timestamp and manage completion state"""
        self.updated_at = datetime.utcnow()
        if self.is_completed and not self.completed_at:
            self.completed_at = datetime.utcnow()
        elif not self.is_completed:
            self.completed_at = None
        return super().save(*args, **kwargs)

    def mark_complete(self):
        """Mark task as completed"""
        self.is_completed = True
        self.completed_at = datetime.utcnow()
        self.save()

    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.is_completed = False
        self.completed_at = None
        self.save()

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and not self.is_completed:
            return datetime.utcnow() > self.due_date
        return False
