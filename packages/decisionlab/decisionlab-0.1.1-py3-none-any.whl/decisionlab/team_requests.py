import ast
import http.client
import os
from ast import literal_eval
from json import JSONDecodeError
from urllib.request import urlopen
import json

BASE_URL = 'https://api.justdecision.com/'
USER_URL_BASE = 'https://api.justdecision.com/v1/public'

TEAMS_BASE_URL = BASE_URL + 'v1/client/decision'
TEAMS_URLS = {
    'get_decision_value': {
        'url': TEAMS_BASE_URL + '/{decision_name}',
        'method': 'GET',
        'body': None
    },
    'update_decision_value': {
        'url': TEAMS_BASE_URL + '/{decision_name}/',
        'method': 'POST',
        'body': {"value": None}
    },
    'list_decisions': {
        'url': TEAMS_BASE_URL + '/names',
        'method': 'GET',
        'body': None
    },
}


def make_api_request(url, method, body, headers):
    body = json.dumps(body)
    conn = http.client.HTTPSConnection("api.justdecision.com")
    if method == 'POST':
        headers['Content-Type'] = 'application/json'
    conn.request(method, url, body, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def get_auth_headers(token=None):
    if not token:
        token = os.environ.get('DECISION_LAB_TOKEN')
    return {
        'Authorization': f'Bearer {token}'
    }


def list_decisions(token=None, private=False, private_definition='_CONFIGURATION'):
    api_data = TEAMS_URLS['list_decisions']
    url = api_data['url']
    method = api_data['method']
    body = api_data['body']
    headers = get_auth_headers(token)
    response = make_api_request(url, method, body, headers)
    data = json.loads(response)
    if data['success']:
        if private:
            return data['decisions']
    return [d for d in data['decisions'] if not d.startswith(private_definition)]


def get_decision_value(decision_name, token=None):
    api_data = TEAMS_URLS['get_decision_value']

    url = api_data['url'].format(decision_name=decision_name)
    method = api_data['method']
    body = api_data['body']

    headers = get_auth_headers(token)

    response = make_api_request(url, method, body, headers)

    try:
        response_data = json.loads(response)
    except JSONDecodeError:
        try:
            response_data = ast.literal_eval(response)
        except (SyntaxError, ValueError):
            return response
    if isinstance(response_data, dict):
        return response_data

    if response.isdigit():
        return int(response)

    if '.' in response and response.replace('.', '', 1).isdigit():
        return float(response)

    return response.strip('"')


def update_decision_value(decision_name, value, token=None):
    api_data = TEAMS_URLS['update_decision_value']
    url = api_data['url'].format(decision_name=decision_name)
    method = api_data['method']
    body = api_data['body']
    body['value'] = value
    headers = get_auth_headers(token)
    return json.loads(make_api_request(url, method, body, headers))
