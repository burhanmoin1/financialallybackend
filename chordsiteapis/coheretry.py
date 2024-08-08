import boto3
import json

bedrock = boto3.client(
  service_name='bedrock-runtime', 
  region_name="us-west-2"
)

prompt = """
We expect OI&E to be around negative $250 million, excluding any potential impact from the mark-to-market of minority investments, and our tax rate to be around 16%. Finally, today, our Board of Directors has declared a cash dividend of $0.24 per share of common stock payable on August 17, 2023, to shareholders of record as of August 14, 2023. With that, let's open the call to questions.
###
Summarize the above conversation.
"""

body = json.dumps({
    "prompt": prompt,
    "max_tokens": 1000,
    "temperature": 0.75,
    "p": 0.9,
    "k": 0,
})

modelId = 'cohere.command-text-v14'
accept = 'application/json'
contentType = 'application/json'

response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())

print(response_body['generations'][0]['text'])