import binascii
import concurrent
import json
import logging

import requests
from google.api_core import retry
import numpy as np
import requests
import yaml
import hashlib
import json
import random
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import pandas as pd
import requests
from .ethic_layer.jailbreak import check_jailbreak
from .ethic_layer.moderation import output_moderation
from .logging import  is_logging_service_active, logging_service_ready_check_url, RemoteLoggingHandler, logging_address

hex_key = '5e99fb38a9f3b6f6496eb07b1e3462cd'

# Convert hexadecimal string to bytes
key_bytes = binascii.unhexlify(hex_key)
pd.set_option('display.max_colwidth', None)


class Light:
    """
    Falcon class provides methods to interact with a specific API,
    allowing operations such as listing models, creating embeddings,
    and generating text based on certain configurations.
    """

    def __init__(self, config):
        """
        Initialize the Falcon object with API key, host name and port, and transport.

        :param api_key: API key for authentication
        :param host_name_port: The host name and port where the API is running
        :param transport: Transport protocol (not currently used)
        """

        self.api_key = config['auth']
        self.api_name = config['name']
        self.api_endpoint = config['type']
        self.url = config['url']
        self.headers = config['headers']
        self.log_id = config['log_id']
        self.use_pil = config['use_pil'] if config['use_pil'] else False
        self.log_key=config['log_key']
        if self.use_pil:
            self.initialise_pil()
        self.start_log(self.log_key)

    def start_log(self,log_key):

        if is_logging_service_active(logging_service_ready_check_url):

            remote_handler = RemoteLoggingHandler(logging_address,log_key)
            # Attach the handler to the self.logger
            logging.basicConfig(level=logging.INFO)  # Set log level to INFO
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(remote_handler)
            self.logger.info("Logging to gateway")
            print("Log Service Enabled")
        else:
            # Fallback to local logging
            logging.basicConfig(filename='falcon.log', level=logging.INFO)
            self.logger = logging.getLogger(__name__)
            self.logger.info("Logging locally because the logging service is not available")
            print("Local Log Service Enabled")

    def current_pil(self):
        return self.use_pil

    def switch_pil(self):
        if (not self.use_pil):
            self.initialise_pil()
        self.use_pil = not self.use_pil
        return f"Switch Success, PIL to {self.use_pil}"

    def list_models(self):
        """
        List the available models from the API.

        :return: A dictionary containing available models.
        """
        if self.api_endpoint == 'dev_quan' or self.api_endpoint == 'dev_full':

            url = f"{self.url}/v1/chat/get_model"
            response = requests.get(url, verify=False)
        elif self.api_endpoint == 'prod':
            self.logger.info(f'{self.log_id}- User Attempt to List Model')
            # TBD
            url = f"{self.url}/v1/chat/get_model"
            response = requests.get(url, verify=False)
            self.logger.info(f'{self.log_id}- List Model Operation Response: {response}')
        else:
            self.logger.info(f'{self.log_id}- Azure Model Listing')

            return {'models': ['gpt-35-turbo-16k-0613-vanilla', 'gpt-35-turbo-0613-vanilla']}

        return response.json()

    def log(self, text):
        self.logger.info(text)

    def initialise_pil(self):
        from presidio_analyzer import AnalyzerEngine

        # Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
        AnalyzerEngine()

    def health(self):
        """
        List the available models from the API.

        :return: A dictionary containing available models.
        """
        if self.api_endpoint == 'dev_quan' or self.api_endpoint == 'dev_full':

            url = f"{self.url}/v1/chat/ping"
            response = requests.get(url, verify=False)
        elif self.api_endpoint == 'prod':
            self.logger.info(f'{self.log_id}- User Attempt to Health Check')
            url = f"{self.url}/v1/chat/ping"
            response = requests.get(url, verify=False)
            self.logger.info(f'{self.log_id}- Health Check Operation Response: {response}')
        else:
            return "Health Check is not available for this API"

        return response.json()

    def create_embedding(self, file_path):
        """
        Create embeddings by sending files to the API.

        :param file_path: Paths of the files to be uploaded
        :return: JSON response from the API
        """
        if self.api_endpoint == 'dev_quan' or self.api_endpoint == 'dev_full':

            url = f"{self.url}/v1/chat/create_embeddingLB"

            # Opening files in read mode
            files = [("file", open(item, "r")) for item in file_path]

            # Preparing data with file extensions
            data = {"extension": ["".join(item.split(".")[-1]) for item in file_path], "type": 'general'}

            headers = self.headers

            # Making a POST request to the API
            response = requests.post(url, headers=headers, verify=False, files=files, data=data)
            response.raise_for_status()  # raising exception for HTTP errors
        elif self.api_endpoint == 'prod':
            # TBD
            self.logger.info(f'{self.log_id}- User Attempt to Create Embedding')

            url = f"{self.url}/v1/chat/create_embeddingLB"

            # Opening files in read mode
            files = [("file", open(item, "r")) for item in file_path]

            # Preparing data with file extensions
            data = {"extension": ["".join(item.split(".")[-1]) for item in file_path], "type": 'general'}

            headers = self.headers

            # Making a POST request to the API
            response = requests.post(url, headers=headers, verify=False, files=files, data=data)
            self.logger.info(f'{self.log_id}- Create Embedding Operation Response: {response}')

            response.raise_for_status()  # raising exception for HTTP errors
        else:
            return "Currently not available for this Service"  # raising exception for HTTP errors

        return response.json()

    @retry.Retry()
    def generate_text(
            self,
            query="",
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
            custom_guardrail=None
    ):
        """
        Generate text by sending data to the API.

        :param chat_history: Chat history for context
        :param query: Query to be asked
        :param use_default: Flag to use default configuration
        :param conversation_config: Conversation configuration parameters
        :param config: Other configuration parameters
        :return: JSON response from the API
        """
        before = []
        after = []
        if custom_guardrail:
            try:
                with open(custom_guardrail, 'r') as file:
                    prime_service = yaml.safe_load(file)
                if not prime_service['custom_handler']:
                    return "Invalid Yaml File"

            except Exception as e:
                return "Invalid Yaml File"
            if 'before' in prime_service['custom_handler'].keys():
                for i in prime_service['custom_handler']['before']:
                    before.append(
                        {'name': i['name'], 'prompt': i['prompt'], 'accept': i['accept'], 'reject': i['reject']})
            if 'after' in prime_service['custom_handler'].keys():
                for i in prime_service['custom_handler']['after']:
                    after.append(
                        {'name': i['name'], 'prompt': i['prompt'], 'accept': i['accept'], 'reject': i['reject']})
        if len(before):
            for i in before:
                print(f'Checking for {i["name"]}')
                prompt = f'''
                {i['prompt']}
                Prompt:
                {query}
                
                
                '''
                response = self.__generate_text__(model=model, query=prompt,
                                                  context=context,
                                                  use_file=0,
                                                  chat_history=chat_history,
                                                  temperature=temperature,
                                                  top_k=top_k,
                                                  frequency_penalty=frequency_penalty,
                                                  repetition_penalty=repetition_penalty,
                                                  presence_penalty=presence_penalty,
                                                  fetch_k=fetch_k,
                                                  select_k=select_k,
                                                  api_version=api_version, )
                response = json.dumps(response)
                if any(context in response for context in i['reject']) and any(
                        context not in response for context in i['accept']):
                    return f"Unable to pass guardrail test {i['name']}"
                print('Pass Check')

        self.logger.info(f'{self.log_id}- User Attempt to Generate Text')
        config = {
            "model": model,
            "temperature": temperature,
            "top_k": top_k,
            "frequency_penalty": frequency_penalty,
            "repetition_penalty": repetition_penalty,
            "presence_penalty": presence_penalty,
            "fetch_k": fetch_k,
            "select_k": select_k,
            "api_version": api_version
        }
        collection = False
        if self.use_pil:
            query, collection = self.__get_pil_text__(query)
            query = query.text
        self.logger.info(
            f'{self.log_id}- Text Query: {query}, Context: {context}, Use File:{use_file}, Chat History:{chat_history}, Config={config}, Guardrail={guardrail}, Service={self.api_endpoint}')
        if guardrail['jailbreak'] or guardrail['moderation']:
            if guardrail['jailbreak']:
                print(f'{self.log_id}- Jailbreak Check Started')
                self.logger.info(
                    f'{self.log_id}- Jailbreak Check Query={query}')

                check_jail = self.__generate_text__(model=model, query=check_jailbreak(query),
                                                    context="",
                                                    use_file=0,
                                                    chat_history=chat_history,
                                                    max_new_tokens=max_new_tokens,
                                                    temperature=temperature,
                                                    top_k=top_k,
                                                    frequency_penalty=frequency_penalty,
                                                    repetition_penalty=repetition_penalty,
                                                    presence_penalty=presence_penalty,
                                                    fetch_k=fetch_k,
                                                    select_k=select_k,
                                                    api_version=api_version,
                                                    )
                self.logger.info(
                    f'{self.log_id}- Jailbreak Check Result {check_jail}')
                print(f'{self.log_id}- Jailbreak Check Result {check_jail}')
                if "yes" in check_jail:
                    self.logger.info(
                        f'{self.log_id}- Jailbreak Check Failed')
                    return "I'm sorry, but I cannot assist with or provide information on any requests that involve breaking moderation or ethical policies, or jailbreaking the model to perform unauthorized actions."
                else:
                    self.logger.info(
                        f'{self.log_id}- Jailbreak Check Success')
            self.logger.info(f'{self.log_id}-Generating Answer')
            response = self.__generate_text__(model=model, query=query,
                                              context=context,
                                              use_file=use_file,
                                              chat_history=chat_history,
                                              temperature=temperature,
                                              top_k=top_k,
                                              frequency_penalty=frequency_penalty,
                                              repetition_penalty=repetition_penalty,
                                              presence_penalty=presence_penalty,
                                              fetch_k=fetch_k,
                                              select_k=select_k,
                                              api_version=api_version, )
            self.logger.info(
                f'{self.log_id}-Generated Answer= {response}')
            if guardrail['moderation']:
                check_moderation = self.__generate_text__(model=model, query=output_moderation(query),
                                                          context="",
                                                          use_file=0,
                                                          chat_history=chat_history,
                                                          temperature=temperature,
                                                          top_k=top_k,
                                                          frequency_penalty=frequency_penalty,
                                                          repetition_penalty=repetition_penalty,
                                                          presence_penalty=presence_penalty,
                                                          fetch_k=fetch_k,
                                                          select_k=select_k,
                                                          api_version=api_version, )
                print(f'{self.log_id}-Moderation Check In Progress')

                self.logger.info(
                    f'{self.log_id}-Moderation Checking Query={check_moderation}')
                if "no" in check_moderation and "yes" not in check_moderation:
                    self.logger.info(f'{self.log_id}-Moderation Checking Failed')

                    return "I'm sorry, but I cannot assist with or provide information on any requests that involve breaking moderation or ethical policies, or jailbreaking the model to perform unauthorized actions."
                else:
                    print(f'{self.log_id}-Moderation Checking Success')

                    self.logger.info(f'{self.log_id}-Moderation Checking Success')
            if self.use_pil:
                response = self.__process_response__pil__(response, collection)
        else:
            self.logger.info(f'{self.log_id}-No Guardrail Done')

            response = self.__generate_text__(model=model, query=query,
                                              context=context,
                                              use_file=0,
                                              chat_history=chat_history,
                                              temperature=temperature,
                                              top_k=top_k,
                                              frequency_penalty=frequency_penalty,
                                              repetition_penalty=repetition_penalty,
                                              presence_penalty=presence_penalty,
                                              fetch_k=fetch_k,
                                              select_k=select_k,
                                              api_version=api_version, )
            self.logger.info(
                f'{self.log_id}-Generated Answer= {response}')
            if self.use_pil:
                response = self.__process_response__pil__(response, collection)
        if len(after):
            for i in after:
                print(f'Checking for {i["name"]}')
                prompt = f'''
                {i['prompt']}
    
    
                Response:
                {query}
    
    
                '''

                response = self.__generate_text__(model=model, query=prompt,
                                                  context=context,
                                                  use_file=0,
                                                  chat_history=chat_history,
                                                  temperature=temperature,
                                                  top_k=top_k,
                                                  frequency_penalty=frequency_penalty,
                                                  repetition_penalty=repetition_penalty,
                                                  presence_penalty=presence_penalty,
                                                  fetch_k=fetch_k,
                                                  select_k=select_k,
                                                  api_version=api_version, )
                response = json.dumps(response)

                if any(context in response for context in i['reject']) and any(
                        context not in response for context in i['accept']):
                    return f"Unable to pass guardrail test {i['name']}"
                print('Pass Check')

        return response

    def __process_response__pil__(self, response, collection):
        json_string = json.dumps(response)

        for i in collection:
            json_string = json_string.replace(f'<{i["text"]}>', i['replace'], 1)
        return json.loads(json_string)

    def __get_pil_text__(self, query):
        from presidio_analyzer import AnalyzerEngine

        # Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
        analyzer = AnalyzerEngine()
        # Call analyzer to get results
        results = analyzer.analyze(text=query,
                                   language='en')
        collect = []

        for index, i in enumerate(results):
            collect.append({'text': i.to_dict()['entity_type'], 'replace': query[i.start:i.end]})

        from presidio_anonymizer import AnonymizerEngine
        from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

        # Initialize the engine with self.logger.
        engine = AnonymizerEngine()

        # Invoke the anonymize function with the text,
        # analyzer results (potentially coming from presidio-analyzer) and
        # Operators to get the anonymization output:
        result = engine.anonymize(
            text=query,
            analyzer_results=results)

        return result, collect

    def __generate_text__(
            self,
            query="Hello",
            context="",
            model="",
            use_file=0,
            chat_history=[],
            max_new_tokens: int = 200,
            temperature: float = 0,
            top_k: int = -1,
            frequency_penalty: int = 0,
            repetition_penalty: int = 1,
            presence_penalty: float = 0,
            fetch_k=100000,
            select_k=4,
            api_version='2023-05-15'

    ):
        """
        Generate text by sending data to the API.

        :param chat_history: Chat history for context
        :param query: Query to be asked
        :param use_default: Flag to use default configuration
        :param conversation_config: Conversation configuration parameters
        :param config: Other configuration parameters
        :return: JSON response from the API
        """

        if self.api_endpoint == 'dev_full':

            url = f"{self.url}/v1/chat/predictCCT"
            # Preparing data to be sent in the request
            config = {
                "query": query,
                "temperature": temperature,
                "top_k": top_k,
                "max_tokens": max_new_tokens,
                "frequency_penalty": frequency_penalty,
                "repetition_penalty": repetition_penalty,
                "presence_penalty": presence_penalty

            }
            data = config
            headers = self.headers  # headers with API key
            # Making a POST request to the API
            response = requests.post(url, headers=headers, verify=False, json=data)
            config = {

                "model": model,
                "temperature": temperature,
                "top_k": top_k,
                "max_tokens": max_new_tokens,
                "frequency_penalty": frequency_penalty,
                "repetition_penalty": repetition_penalty,
                "presence_penalty": presence_penalty

            }
            experiment = self.__aesencode__(config)
            response.raise_for_status()  # raising exception for HTTP errors
            result = response.json()
            result['experiment_id'] = experiment
            return result  # returning JSON response



        elif self.api_endpoint == 'dev_quan':

            url = f"{self.url}/v1/chat/predictLB"
            # Preparing data to be sent in the request
            config = {
                "query": query,
                "config": {
                    "model": model,
                    "temperature": temperature,
                    "top_k": top_k,
                    "max_new_tokens": max_new_tokens,
                    "batch_size": 256,
                    "top_p": 1},
                "chat_history": chat_history,
                "use_default": 1,
                "use_file": use_file,
                "conversation_config": {
                    "k": select_k,
                    "fetch_k": fetch_k,
                    "bot_context_setting": context
                },
                "type": 'general'

            }
            data = config
            headers = self.headers  # headers with API key
            # Making a POST request to the API
            response = requests.post(url, headers=headers, verify=False, json=data)
            config = {

                          "model": model,
                          "max_new_tokens": max_new_tokens,
                          "temperature": temperature,
                          "top_k": top_k,
                          "top_p": 1,
                          "batch_size": 256

                      }
            experiment = self.__aesencode__(config)
            response.raise_for_status()  # raising exception for HTTP errors
            result = response.json()
            result['experiment_id'] = experiment
            return result  # returning JSON response

        elif self.api_endpoint == 'prod':
            url = f"{self.url}/v1/chat/predictLB"
            # Preparing data to be sent in the request
            type = 'general'
            data = {
                "chat_history": chat_history,
                "query": query,
                "use_default": 1,
                'use_file': use_file,
                "conversation_config": {"k": select_k,
                                        "fetch_k": fetch_k,
                                        "bot_context_setting": context},
                "config": {
                    "model": model,
                    "max_new_tokens": max_new_tokens,
                    "temperature": temperature,
                    "top_p": 1,
                    "batch_size": 256

                },
                'type': type
            }

            headers = self.headers  # headers with API key
            # Making a POST request to the API
            response = requests.post(url, headers=headers, verify=False, json=data)
            config = {
                      "config": {
                          "model": model,
                          "max_new_tokens": max_new_tokens,
                          "temperature": temperature,
                          "top_p": 1,
                          "batch_size": 256

                      },
                      'type': type}
            experiment = self.__aesencode__(config)
            response.raise_for_status()  # raising exception for HTTP errors
            result = response.json()
            result['experiment_id'] = experiment
            return result  # returning JSON response
        elif self.api_endpoint == 'azure':
            response = requests.post(
                url=f"{self.url}/openai/deployments/{model}/chat/completions?api-version={api_version}",
                headers=self.headers, json=
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant."
                        },
                        {
                            "role": "user",
                            "content": f"{query}"
                        },

                    ],
                    "frequency_penalty": frequency_penalty,
                    "temperature": temperature,
                    "max_tokens": max_new_tokens
                }
            )
            config = {"model": model,

                "frequency_penalty": frequency_penalty,
                      "temperature": temperature,
                      "max_tokens": max_new_tokens}
            experiment = self.__aesencode__(config)
            response.raise_for_status()  # raising exception for HTTP errors
            result = response.json()
            result['experiment_id'] = experiment
            return result  # returning JSON response

    def __generate_parameter_combinations__(self,param_values):
        param_names = list(param_values.keys())
        param_ranges = list(param_values.values())

        # Generate combinations of parameter values
        combinations = list(product(*(v if isinstance(v, (range, list)) else [v] for v in param_ranges)))

        param_combinations = []
        for combo in combinations:
            param_combination = dict(zip(param_names, combo))
            param_combinations.append(param_combination)

        return param_combinations

    def evaluate_parameter(self, config):
        if (not config['model'] or not config['query']):
            return "Failed: You need to provide the model and query you want to test."

        data = {
            'experiment': [],
            'config': [],
            'query': [],
            'model': [],
            'result': []
        }
        df = pd.DataFrame(data)
        param_test = self.__generate_parameter_combinations__(config)

        def generate_and_append_text(params):
            response = self.generate_text(**params)
            new_row = {
                'experiment': self.__aesencode__(params),
                'config': params,
                'query': params['query'],
                'model': params['model'],
                'result': response
            }
            return new_row

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_params = {executor.submit(generate_and_append_text, i): i for i in param_test}
            for future in concurrent.futures.as_completed(future_to_params):
                params = future_to_params[future]
                try:
                    new_row = future.result()
                    df = df.append(new_row, ignore_index=True)
                except Exception as e:
                    print(f"An error occurred: {e}")

        return df

    def __aesencode__(self, input_dict):
        text = json.dumps(input_dict, sort_keys=True)
        # Convert the dictionary to a string using JSON
        cipher = AES.new(key_bytes, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
        result=cipher.nonce + tag + ciphertext
        result=result.hex()
        return result

    def decrypt_hash(self, encrypted_data):
        encrypted_data=binascii.unhexlify(encrypted_data)
        nonce = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        cipher = AES.new(key_bytes, AES.MODE_EAX, nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode('utf-8')
