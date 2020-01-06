import os
import base64

from google.cloud import kms

SECRET_STRING = b'The chickens are in the hayloft.'

def get_secret():
    kms_client = kms.KeyManagementServiceClient()
    return kms_client.decrypt(
        os.environ["SECRET_RESOURCE_NAME"],
        base64.b64decode(os.environ["SECRET_API_TOKEN"]),
    ).plaintext

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    secret_string = get_secret()

    request_json = request.get_json()
    if request.args and 'name' in request.args:
        name = request.args.get('name')
        return f'Hello {name}! {secret_string}'
    elif request_json and 'name' in request_json:
        name = request_json.get('name')
        return f'Hello {name}! {secret_string}'
    else:
        return f'Hello World! {secret_string}'
