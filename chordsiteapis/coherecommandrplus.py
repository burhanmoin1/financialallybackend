# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use the Cohere Command R model.
"""
import json
import logging
import boto3
from botocore.exceptions import ClientError

def generate_text(model_id, body):
    """
    Generate text using a Cohere Command R model.
    Args:
        model_id (str): The model ID to use.
        body (str) : The request body to use.
    Returns:
        dict: The response from the model.
    """

    bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    return response

def main():
    """
    Entrypoint for Cohere example.
    """
    model_id = 'cohere.command-r-plus-v1:0'
    message = "We expect OI&E to be around negative $250 million, excluding any potential impact from the mark-to-market of minority investments, and our tax rate to be around 16%. Finally, today, our Board of Directors has declared a cash dividend of $0.24 per share of common stock payable on August 17, 2023, to shareholders of record as of August 14, 2023. With that, let's open the call to questions.\n###\nSummarize the above conversation."

    try:
        body = json.dumps({
            "message": message,
            "max_tokens": 512,
            "temperature": 0.5,
            "p": 0.01,
            "k": 0
        })
        response = generate_text(model_id=model_id, body=body)

        response_body = json.loads(response.get('body').read())
        print(f"\n{response_body.get('text', 'No text returned')}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occurred: " + format(message))

if __name__ == "__main__":
    main()
