import requests

import logging


def is_logging_service_active(url):
    try:
        response = requests.get(url)
        return response.status_code // 100 == 2  # Check if status code is in 200 range
    except:
        return False


import logging
import requests
import json


class RemoteLoggingHandler(logging.Handler):
    def __init__(self, url,auth_key):
        super().__init__()
        self.url = url
        self.auth_key=auth_key

    def emit(self, record):
        log_entry = self.format(record)
        payload = {'log_entry': log_entry}

        try:
            response = requests.post(self.url, data=json.dumps(payload), headers={'X-API-Key':self.auth_key})
            if response.status_code != 200:
                print(f"Failed to send log entry. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending log entry: {e}")

logging_service_ready_check_url='http://10.142.91.197:8443/aiaas_llm/v1/chat/ping'
logging_address='http://10.142.91.197:8443/flog/falcon_logger'

