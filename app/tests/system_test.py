import os
import uuid

import requests

import app.main as main

def test_no_args():
    GCLOUD_TOKEN = os.getenv('GCLOUD_TOKEN')
    assert GCLOUD_TOKEN is not None
    BASE_URL = os.getenv('BASE_URL')
    assert BASE_URL is not None

    res = requests.get(
        '{}/hello_world'.format(BASE_URL),
        headers={'Authorization': f'Bearer {GCLOUD_TOKEN}'},
    )
    assert res.text == 'Hello World! {}'.format(main.SECRET_STRING)


def test_args():
    GCLOUD_TOKEN = os.getenv('GCLOUD_TOKEN')
    assert GCLOUD_TOKEN is not None
    BASE_URL = os.getenv('BASE_URL')
    assert BASE_URL is not None

    name = str(uuid.uuid4())
    res = requests.post(
      '{}/hello_world'.format(BASE_URL),
      headers={'Authorization': f'Bearer {GCLOUD_TOKEN}'},
      json={'name': name}
    )
    assert res.text == 'Hello {}! {}'.format(name, main.SECRET_STRING)
