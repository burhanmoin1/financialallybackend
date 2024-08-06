from django_mongoengine import Document, fields
from datetime import datetime

class User(Document):
    email = fields.EmailField(blank=False, unique=True)
    first_name = fields.StringField(blank=False)
    last_name = fields.StringField(blank=False)
    password = fields.StringField(blank=False)
    is_activated = fields.BooleanField(default=False)
    activation_token = fields.StringField(blank=True)
    activation_token_valid = fields.BooleanField(blank=True, default=True)
    password_reset_token = fields.StringField(blank=True)
    password_reset_token_valid = fields.BooleanField(blank=True, default=False)
