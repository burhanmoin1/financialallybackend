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
model_id = "cohere.command-text-v14"

# Start a conversation with the user message.
user_message = """Extract the band name from the contract:

This Music Recording Agreement ("Agreement") is made effective as of the 13 day of December, 2021 by and between Good Kid, a Toronto-based musical group (“Artist”) and Universal Music Group, a record label with license number 545345 (“Recording Label"). Artist and Recording Label may each be referred to in this Agreement individually as a "Party" and collectively as the "Parties." Work under this Agreement shall begin on March 15, 2022.
"""
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId="cohere.command-text-v14",
        messages=conversation,
        inferenceConfig={"maxTokens":200,"temperature":0.9,"topP":1},
        additionalModelRequestFields={"k":0}
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)