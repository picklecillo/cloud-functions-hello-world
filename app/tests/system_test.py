import os
import uuid

import requests


config = {
    'jira_api_url': 'https://5e136df66e229f00146795e2.mockapi.io/rest/api/2/',
}


def test_no_args():
    GCLOUD_TOKEN = os.getenv('GCLOUD_TOKEN')
    assert GCLOUD_TOKEN is not None
    BASE_URL = os.getenv('BASE_URL')
    assert BASE_URL is not None

    res = requests.get(
        '{}/hello_world'.format(BASE_URL),
        headers={'Authorization': f'Bearer {GCLOUD_TOKEN}'},
    )
    assert res.content.decode() == str(config)
