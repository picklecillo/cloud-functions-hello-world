import requests
import os

from kms import get_config

BASE_URL = get_config()['jira_api_url']


def get_issues():
    response = requests.get(BASE_URL + 'issue')
    return response.json()

def get_single_issue(issue_id):
    response = requests.get(BASE_URL + 'issue/' + str(issue_id))
    return response.json()

def set_issue(data):
    response = requests.post(BASE_URL + 'issue', data=data)

    return response.json()

def delete_issue(issue_id):
    response = requests.delete(BASE_URL + 'issue/' + str(issue_id))

    return response.json()