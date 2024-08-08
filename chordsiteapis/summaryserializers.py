from rest_framework import serializers

class PromptSerializer(serializers.Serializer):
    prompt = serializers.CharField()

from .models import TextSummarizationHistory

class TextSummarizationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TextSummarizationHistory
        fields = ['user', 'summary']

class RetrieveTextSummarizationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TextSummarizationHistory
        fields = ['summary']