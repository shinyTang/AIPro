import json
import openai
import os
import requests
import time

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

MAX_LEN = 2048

prompt_prefix = """
你是一个客服，回答用户关于文档的问题。
仅使用以下资料提供的事实进行回答。 如果下面没有足够的信息，就说你不知道。不要生成不使用以下资料的答案。

资料：
{sources}
"""
summary_prompt_template =  """
新问题：{question}
"""

# Including the api-key in HTTP headers
headers =  {"api-key": openai_api_key}

def get_chat_answer(messages: dict, max_token=1024):
    return openai.ChatCompletion.create(
        engine="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=max_token,
    )["choices"][0]["message"]


if __name__ == "__main__":  
    star = time.time()    
    print(f"Time taken: {time.time() - star}")

    history = []
    user_input = ""

    while(True):
        user_input = input()
        if len(history) == 0:
            query = user_input
       
        history.append({"role": "user", "content": user_input})
        massage = history
        res = get_chat_answer(massage)
        print(res["content"])

        #     query = get_chat_answer(
        #         history
        #         + [
        #             {
        #                 "role": "user",
        #                 "content": summary_prompt_template.format(question=user_input),
        #             }
        #         ],
        #         max_token=32,
        #     )["content"]
       
        # print(f"Searching: {query}")        




# try:
#     # Request for creating a completion for the provided prompt and parameters
#     response = requests.post(api_url, json=json_data, headers=headers)
#     completion = response.json()
    
#     print(completion)

#     # print the completion
#     print(completion['choices'][0]['text'])
    
#     # Here indicating if the response is filtered
#     if completion['choices'][0]['finish_reason'] == "content_filter":
#         print("The generated content is filtered.")
# except:
#     print("An exception has occurred. \n")
#     print("Error Message:", completion['error']['message'])



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