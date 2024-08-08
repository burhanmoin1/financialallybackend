import boto3
import json

brt = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")

body = json.dumps({
    "prompt": "We expect OI&E to be around negative $250 million, excluding any potential impact from the mark-to-market of minority investments, and our tax rate to be around 16%. Finally, today, our Board of Directors has declared a cash dividend of $0.24 per share of common stock payable on August 17, 2023, to shareholders of record as of August 14, 2023. With that, let's open the call to questions.\n###\nSummarize the above conversation.",
    "maxTokens": 200,
    "temperature": 0.5,
    "topP": 0.5
})

modelId = 'ai21.j2-mid-v1'
accept = 'application/json'
contentType = 'application/json'

response = brt.invoke_model(
    body=body, 
    modelId=modelId, 
    accept=accept, 
    contentType=contentType
)

response_body = json.loads(response.get('body').read())

# text
print(response_body.get('completions')[0].get('data').get('text'))