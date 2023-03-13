import json
import requests

def lambda_handler(event, context):
    api_key = "your_api_key" # replace with your API key
    
    # Get request to first API endpoint with api_key as query parameter
    response = requests.get('https://example.com/first_api_endpoint', params={"api_key": api_key})
    data = response.json()
    
    # POST request to second API endpoint with data from first API response
    post_data = {
        'key1': data['value1'],
        'key2': data['value2'],
        'key3': 'value3'
    }
    headers = {'Content-Type': 'application/json'}
    post_response = requests.post('https://example.com/second_api_endpoint', data=json.dumps(post_data), headers=headers)
    
    return {
        'statusCode': post_response.status_code,
        'body': post_response.text
    }
