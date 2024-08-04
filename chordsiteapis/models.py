from django_mongoengine import Document, fields
from datetime import datetime

class User(Document):
    email = fields.EmailField(blank=False, unique=True)
    first_name = fields.StringField(blank=False)
    last_name = fields.StringField(blank=False)
    password = fields.StringField(blank=False)
    is_active = fields.BooleanField(default=False)
    token = fields.StringField(blank=True)
    login_time = fields.DateTimeField(blank=True)
