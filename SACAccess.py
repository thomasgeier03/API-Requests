import os
import http.client
import base64
import json
from datetime import datetime, timedelta

def save_to_env(key, value):
    with open('api.env', 'r') as file:
        lines = file.readlines()

    with open('api.env', 'w') as file:
        key_written = False
        for line in lines:
            if line.startswith(f'{key}='):
                file.write(f'{key}={value}\n')
                key_written = True
            else:
                file.write(line)

        if not key_written:
            file.write(f'{key}={value}\n')

def load_token():
    token = None
    timestamp = None
    if os.path.exists('api.env'):
        with open('api.env', 'r') as file:
            for line in file:
                if line.startswith('bearer_token='):
                    token = line.strip().split('=')[1]
                elif line.startswith('bearer_timestamp='):
                    timestamp = datetime.fromisoformat(line.strip().split('=')[1])
    return token, timestamp

def get_bearer_token():
    token, timestamp = load_token()
    if token and timestamp and datetime.now() - timestamp < timedelta(hours=1):
        print('Bearer Token loaded')
        return token
    else:
        conn = http.client.HTTPSConnection(f"{os.getenv('SACTokenURL')}")
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{os.getenv('User')}:{os.getenv('Secret')}".encode('utf-8')).decode('utf-8')
        }
        payload = 'grant_type=client_credentials'

        conn.request("GET", "/oauth/token?response_type=token&grant_type=client_credentials", payload, headers)
        response = conn.getresponse()
        data = response.read()

        if response.status == 200:
            bearer_token = json.loads(data.decode("utf-8")).get('access_token')
            save_to_env('bearer_token', bearer_token)
            save_to_env('bearer_timestamp', datetime.now().isoformat())
            print('Bearer Token saved')
            return bearer_token
        else:
            raise Exception(f"Failed to get bearer token: {response.status} {data.decode('utf-8')}")

# X-CSRF-Token API-Aufruf
def get_xcsrf_token():
    bearer_token = get_bearer_token()
    conn = http.client.HTTPSConnection(f"{os.getenv('SACServiceURL')}")
    headers = {
        'x-csrf-token': 'fetch',
        'x-sap-sac-custom-auth': 'true',
        'Authorization': f'Bearer {bearer_token}'
    }
    
    conn.request("GET", "/api/v1/csrf", headers=headers)
    response = conn.getresponse()
    data = response.read()
    
    if response.status == 200:
        xcsrf_token = response.getheader('x-csrf-token')
        if xcsrf_token:
            save_to_env('x-csrf-token', xcsrf_token)
            print('X-CSRF-Token saved')
            return xcsrf_token
    else:
        raise Exception(f"Failed to get X-CSRF-Token: {response.status} {data.decode('utf-8')}")