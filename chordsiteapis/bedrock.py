# Use the Converse API to send a text message to Llama 2 Chat 70B.
from django.conf import settings
import boto3
from botocore.exceptions import ClientError

client = boto3.client(
    'bedrock-runtime',
    region_name='us-west-2',
    aws_access_key_id = 'AKIAZKYLDIPKA7NEASUJ',
    aws_secret_access_key = 'uGSV2yWnZwNJq4DhOcEQ0dE2Rs2qixlFFLr0zJct'
)
# Set the model ID, e.g., Titan Text Premier.
model_id = "meta.llama2-70b-chat-v1"

# Start a conversation with the user message.
user_message = """[INST]You are an economist with access to lots of data[/INST]
Write an article about impact of high inflation to GDP of a country"""
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId="meta.llama2-70b-chat-v1",
        messages=conversation,
        inferenceConfig={"maxTokens":512,"temperature":0.5,"topP":0.9},
        additionalModelRequestFields={}
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)