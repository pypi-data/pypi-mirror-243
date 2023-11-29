![AIaaS Falcon Logo](img/AIAAS_FALCON.jpg)

# AIaaS Falcon-Light


<h4 align="center">
    <p>
        <a href="#shield-installation">Installation</a> |
        <a href="#fire-quickstart">Quickstart</a> |
    <p>
</h4>


![Documentation Coverage](interrogate_badge.svg)

## Description

AIaaS_Falcon_Light is Generative AI - Logical & logging framework support AIaaS Falcon library

## :shield: Installation

Ensure you have the `requests` and `google-api-core` libraries installed:

```bash
pip install aiaas-falcon-light
```


if you want to install from source

```bash
git clone https://github.com/Praveengovianalytics/falcon_light && cd falcon_light
pip install -e .
```

### Methods
### `Light`  Class
- `__init__ (config)`
Intialise the Falcon object with endpoint configs. \
Parameter: 
     - config: A object consisting parameter:
        - api_key : API Key
        - api_name: Name for endpoint
        - api_endpoint: Type of endpoint ( can be azure, dev_quan, dev_full, prod)
        - url: url of endpoint (eg: http://localhost:8443/)
        - log_id: ID of log (Integer Number)
        - use_pil: Activate Personal Identifier Information Limit Protection (Boolean)
        - headers: header JSON for endpoint

- `current_pil()`
Check current Personal Identifier Information Protection activation status

- `switch_pil()`
Switch current Personal Identifier Information Protection activation status
- `list_models()`
List out models available
- `initalise_pil()`
Download and intialise PII Protection. \
Note: This does not activate PII but initialise dependencies

- `health()`
Check health of current endpoint

- `create_embedding(file_path)`
Create embeddings by sending files to the API. \
Parameter:
    - file_path: Path to file 

- `generate_text(query="",
            context="",
            use_file=0,
            model="",
            chat_history=[],
            max_new_tokens: int = 200,
            temperature: float = 0,
            top_k: int = -1,
            frequency_penalty: int = 0,
            repetition_penalty: int = 1,
            presence_penalty: float = 0,
            fetch_k=100000,
            select_k=4,
            api_version='2023-05-15',
            guardrail={'jailbreak': False, 'moderation': False},
            custom_guardrail=None)` \
  Generate text using LLM endpoint. Note: Some parameter of the endpoint is endpoint-specific. \
  Parameter: 
  - query: a string of your prompt
  - use_file: Whether to take file to context in generation. Only applies to dev_full and dev_quan. Need to `create_embedding` before use.
  - model: a string on the model to use. You can use ` list_models` to check for model available.
  - chat_history: an array of chat history between user and bot. Only applies to dev_full and dev_quan. (Beta)
  - max_new_token: maximum new token to generate. Must be integer.
  - temperature: Float that controls the randomness of the sampling. Lower
        values make the model more deterministic, while higher values make
        the model more random. Zero means greedy sampling.
  - top_k: Integer that controls the number of top tokens to consider.
  - frequency_penalty: Float that penalizes new tokens based on their
        frequency in the generated text so far.
  - repetition_penalty: Float that penalizes new tokens based on whether
        they appear in the prompt and the generated text so far.
  - presence_penalty: Float that penalizes new tokens based on whether they
        appear in the generated text so far
  - fetch_k: Use for document retrival. Include how many element in searching. Only applies when `use_file` is 1
  - select k: Use to select number of document for document retrieval. Only applies when `use_file` is 1
  - api_version: Only applies for azure endpoint
  - guardrail: Whether to use the default jailbreak guardrail and moderation guardrail
  - custom_guardrail: Path to custom guardrail .yaml file. The format can be found in sample.yaml
  
- ` evaluate_parameter(config)`
Carry out grid search for parameter \
Parameter:
    - config: A dict. The dict must contain model and query. Parameter to grid search must be a list. 
        - model: a string of model
        - query: a string of query
        - **other parameter (eg: "temperature":list(np.arange(0,2,0.5))
- `decrypt_hash(encrypted_data)`
Decret the configuration from experiment id.
Parameter:
    - encrypted_data: a string of id

## :fire: Quickstart

```
from aiaas_falcon import Falcon
model=Falcon(api_name="azure_1",protocol='https',host_name_port='example.com',api_key='API_KEY',api_endpoint='azure')
model.list_models()
model.generate_text_full(query="Hello, introduce yourself",model='gpt-35-turbo-0613-vanilla',api_version='2023-05-15')
```

## Conclusion

AIaaS_Falcon_Light library simplifies interactions with the AIaaS Falcon, providing a straightforward way to perform various operations such as fact-checking and logging.

## Authors

- [@Praveengovianalytics](https://github.com/Praveengovianalytics)
- [@zhuofan](https://github.com/zhuofan-16)

## Google Colab

- [Get start with aiaas_falcon](https://colab.research.google.com/drive/1haZ-1fD4htQuNF2zzyrUSTP90KRls1dC?usp=sharing)

## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
