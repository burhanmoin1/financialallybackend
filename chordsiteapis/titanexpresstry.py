import json
import logging
import boto3
from botocore.exceptions import ClientError

class TextGenerationError(Exception):
    pass

def generate_text(model_id, body):
    """
    Generate text using the model on demand.
    Args:
        model_id (str): The model ID to use.
        body (str): The request body to use.
    Returns:
        str: The generated text from the model.
    """
    bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    try:
        response = bedrock.invoke_model(
            body=body, modelId=model_id, accept="application/json", contentType="application/json"
        )
        response_body = json.loads(response.get("body").read())
        
        if 'error' in response_body:
            raise TextGenerationError(f"Text generation error: {response_body['error']}")
        
        # Assuming response_body['results'] contains the required information
        return response_body['results'][0]['outputText']
    
    except ClientError as e:
        logging.error(f"ClientError: {e}")
        raise
    except TextGenerationError as e:
        logging.error(f"TextGenerationError: {e}")
        raise

def main():
    """
    Entrypoint for the example.
    """
    model_id = 'amazon.titan-text-lite-v1'
    prompt = """We expect OI&E to be around negative $250 million, excluding any potential impact from the mark-to-market of minority investments, and our tax rate to be around 16%. Finally, today, our Board of Directors has declared a cash dividend of $0.24 per share of common stock payable on August 17, 2023, to shareholders of record as of August 14, 2023. With that, let's open the call to questions.
###
Summarize the above conversation. """

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "stopSequences": [],
            "temperature": 0.5,
            "topP": 0.01
        }
    })

    try:
        summary = generate_text(model_id, body)
        print(f"Summary: {summary}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
