from rest_framework_mongoengine import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

from .models import TextSummarizationHistory
class TextSummarizationHistorySerializer(serializers.DocumentSerializer):
    class Meta:
        model = TextSummarizationHistory
        fields = ['summary']

    def validate(self, data):
        # You can add custom validation logic here if needed
        return data

# Serializer for retrieving summaries
class RetrieveTextSummarizationHistorySerializer(serializers.DocumentSerializer):
    class Meta:
        model = TextSummarizationHistory
        fields = ['summary']
