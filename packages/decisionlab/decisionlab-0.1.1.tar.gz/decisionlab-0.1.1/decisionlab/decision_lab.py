import os
from ast import literal_eval
import requests

from .team_requests import list_decisions
from .team_requests import get_decision_value
from .team_requests import update_decision_value
from .team_requests import USER_URL_BASE


class DecisionLab:
    def __init__(self, *, token=None, is_read_write=False):
        self.token = token or os.environ.get('DECISION_LAB_TOKEN')
        if not self.token:
            raise ValueError("A token must be provided or set as an environment variable 'DECISION_LAB_TOKEN'")
        self.is_read_write = is_read_write

    def list_decisions(self, private=False, private_definition='_CONFIGURATION'):
        if self.is_read_write:
            return list_decisions(self.token, private=private, private_definition=private_definition)
        response = requests.get(f'{USER_URL_BASE}/{self.token}')
        return response.json()

    def update_decision_value(self, decision_name, value):
        if not self.is_read_write:
            raise PermissionError("Read-write token is required for this operation.")
        return update_decision_value(decision_name, value, self.token)

    def get_decision(self, decision_name):
        if self.is_read_write:
            return get_decision_value(decision_name, self.token)
        response = requests.get(f'{USER_URL_BASE}/{self.token}/{decision_name}')
        response_json = response.json()

        if isinstance(response_json, dict) and response_json.get('success') is False:
            return []

        if isinstance(response_json, str):
            try:
                response_json = literal_eval(response_json)
            except (ValueError, SyntaxError):
                pass

        return response_json
