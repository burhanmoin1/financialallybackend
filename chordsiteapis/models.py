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
    session_tokens = fields.ListField(fields.StringField(), blank=True, default=list)  # Corrected order

    def add_session_token(self, token):
        # Add a new session token if there are less than 4
        if len(self.session_tokens) < 4:
            self.session_tokens.append(token)
        else:
            # If there are already 4 tokens, remove the oldest and add the new one
            self.session_tokens.pop(0)
            self.session_tokens.append(token)
        self.save()
    
    def remove_session_token(self, token):
        # Remove a specific session token
        if token in self.session_tokens:
            self.session_tokens.remove(token)
            self.save()
    
    def is_session_token_valid(self, token):
        # Check if a session token is valid
        return token in self.session_tokens
