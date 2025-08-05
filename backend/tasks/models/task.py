from mongoengine import Document, StringField, DateTimeField

class Task(Document):
    title = StringField(required=True, max_length=200)
    description = StringField()
    due_date = DateTimeField()
    status = StringField(choices=["pending", "completed"], default="pending")
