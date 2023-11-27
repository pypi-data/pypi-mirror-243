# KBRaiN SDK API

The KBRaiN SDK API is a Python library that provides a simple interface to interact with the KBRaiN services. It includes methods for account creation, key generation, and interacting with the OpenAI chat service.

## Installation

To install the KBRaiN SDK API, use pip:

```bash
pip install kbrainsdk
```

## Usage
First, import the library and create an instance of the API client:

```python
from kbrainsdk.api import KBRaiNAPI

kbrain = KBRaiNAPI(account_id='your_account_id', api_key='your_api_key', base_url="kbrain_base_url")
```

We recommend using environment variables or a tool like Azure Key Vault to inject your api key, do not commit your api key to any source control for security reasons.

You can also skip passing in values to the constructor and KBRaiN will reference your environment variables if they are defined with the following names:

```bash
KBRAIN_BASE_URL
KBRAIN_ACCOUNT_ID
KBRAIN_API_KEY
```

## OpenAI Chat
To interact with the OpenAI chat API, use the openai_chat method. This method takes the same arguments as the OpenAI API as of version `1.3.3`. You can see the API documentation at [OpenAI](https://platform.openai.com/docs/api-reference/chat) for details.

Here is an example:

```python
messages = [{
    'role': 'system',
    'content': 'You are a helpful assistant.'
}, {
    'role': 'user',
    'content': 'What is the air speed velocity of an unladen swallow?'
}]

model_name = 'gpt-3.5-turbo'  # Replace with the model name in the targeted Azure OpenAI Resource. This should be chat for gpt-3x and chat-4 for gpt4. 
model_type = 'openai'  # Replace with your model type
deployment_id = 'chat'

response = kbrain.llms.openai_chat(messages, model_name, model_type, deployment_id)

print(response["response"])
print(response["tokens"])
```

## OpenAI Completion
To interact with the OpenAI completions API, use the openai_completion method. This method takes the same arguments as the OpenAI API as of version `1.3.3`. You can see the API documentation at [OpenAI](https://platform.openai.com/docs/api-reference/chat) for details.

Here is an example:

```python

prompt = "Translate this into Spanish: Hello World!"
model_name = 'gpt-3.5-instruct'  # Replace with the model name in the targeted Azure OpenAI Resource. This should be chat for gpt-3x and chat-4 for gpt4. 
model_type = 'openai'  # Replace with your model type
deployment_id = 'instruct'

response = kbrain.llms.openai_completion(prompt, model_name, model_type, deployment_id)

print(response["response"])
print(response["tokens"])
```

## Dataset Features

To interact with the Dataset features, follow the example below:



```python
email = "<your users email>"
token = "<your users authentication token into your app>"
client_id = "<your apps client_id>"
oauth_secret = "<your apps oauth secret>"
tenant_id = "<your apps tenant id>"
response = kbrain.datasets.list_datasets(email, token, client_id, oauth_secret, tenant_id)
```


## License
Copyright 2023, KBR Inc.