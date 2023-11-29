import pytest
import responses
from decision_lab import DecisionLab

# Define test data and URLs
TEST_UUID = '4c8fc261-92de-4dea-8ed8-9418a577d503'
URL_BASE = 'https://api.justdecision.com/v1/public'
DECISION_LIST_URL = f'{URL_BASE}/{TEST_UUID}'
DECISION_NAME = 'test_decision'
DECISION_URL = f'{URL_BASE}/{TEST_UUID}/{DECISION_NAME}'
DECISION_LIST_RESPONSE = ['decision1', 'decision2']
DECISION_RESPONSE = {'success': True, 'value': 'decision_value'}


# Use the responses library to mock the API responses
@responses.activate
def test_get_decisions_list():
    responses.add(responses.GET, DECISION_LIST_URL, json=DECISION_LIST_RESPONSE, status=200)
    decision_lab = DecisionLab(uuid=TEST_UUID)
    result = decision_lab.get_decisions_list()
    assert result == DECISION_LIST_RESPONSE


@responses.activate
def test_get_decision():
    responses.add(responses.GET, DECISION_URL, json=DECISION_RESPONSE, status=200)
    decision_lab = DecisionLab(uuid=TEST_UUID)
    result = decision_lab.get_decision(DECISION_NAME)
    assert result == DECISION_RESPONSE


@responses.activate
def test_get_decision_not_found():
    responses.add(responses.GET, DECISION_URL, json={'success': False, 'error': 'Not found'}, status=404)
    decision_lab = DecisionLab(uuid=TEST_UUID)
    result = decision_lab.get_decision(DECISION_NAME)
    assert result == []


def test_missing_uuid():
    with pytest.raises(ValueError) as exc_info:
        DecisionLab(uuid=None)
    assert str(exc_info.value) == "UUID must be provided or set as an environment variable 'DECISION_LAB_UUID'"
