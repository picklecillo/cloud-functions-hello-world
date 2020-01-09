from unittest.mock import Mock

from function import main


def test_get_config():
    name = 'test'
    data = {'jira_api_url': 'https://5e136df66e229f00146795e2.mockapi.io/rest/api/2/'}
    req = Mock(get_json=Mock(return_value=data), args=data)

    assert main.hello_world(req) == str({'jira_api_url': 'https://5e136df66e229f00146795e2.mockapi.io/rest/api/2/'})
