import json
import openai
import os
import requests

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai_api_version = "2023-03-15-preview"
openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")

deployment_name = "text-davince-002"

#Reset API
api_url = f"{openai_api_base}/openai/deployments/{deployment_name}/completions?api-version={openai_api_version}"
print(api_url)

# Example prompt for request payload
prompt = "Hello world"

# Json payload
# To know more about the parameters, checkout this documentation: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference
json_data = {
  "prompt": prompt,
  "temperature":0,
  "max_tokens": 30
}

# Including the api-key in HTTP headers
headers =  {"api-key": openai_api_key}

try:
    # Request for creating a completion for the provided prompt and parameters
    response = requests.post(api_url, json=json_data, headers=headers)
    completion = response.json()
    
    print(completion)

    # print the completion
    print(completion['choices'][0]['text'])
    
    # Here indicating if the response is filtered
    if completion['choices'][0]['finish_reason'] == "content_filter":
        print("The generated content is filtered.")
except:
    print("An exception has occurred. \n")
    print("Error Message:", completion['error']['message'])



# Completion.create
# prompt = "Hello world"

# try:
#     # Create a completion for the provided prompt and parameters
#     # To know more about the parameters, checkout this documentation: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference
#     completion = openai.Completion.create(
#                     prompt=prompt,
#                     temperature=0,
#                     max_tokens=30,
#                     engine=deployment_name)

#     # print the completion
#     print(completion.choices[0].text.strip(" \n"))
    
#     # Here indicating if the response is filtered
#     if completion.choices[0].finish_reason == "content_filter":
#         print("The generated content is filtered.")
        
# except openai.error.APIError as e:
#     # Handle API error here, e.g. retry or log
#     print(f"OpenAI API returned an API Error: {e}")

# except openai.error.AuthenticationError as e:
#     # Handle Authentication error here, e.g. invalid API key
#     print(f"OpenAI API returned an Authentication Error: {e}")

# except openai.error.APIConnectionError as e:
#     # Handle connection error here
#     print(f"Failed to connect to OpenAI API: {e}")

# except openai.error.InvalidRequestError as e:
#     # Handle connection error here
#     print(f"Invalid Request Error: {e}")

# except openai.error.RateLimitError as e:
#     # Handle rate limit error
#     print(f"OpenAI API request exceeded rate limit: {e}")

# except openai.error.ServiceUnavailableError as e:
#     # Handle Service Unavailable error
#     print(f"Service Unavailable: {e}")

# except openai.error.Timeout as e:
#     # Handle request timeout
#     print(f"Request timed out: {e}")