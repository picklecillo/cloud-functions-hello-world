import os
import json
import logging
import base64
from google.cloud import storage
from googleapiclient import discovery

from .settings import CONFIG_PATH

enable_logging = True

# Change the format of messages logged to Stackdriver
logging.basicConfig(format='%(message)s', level=logging.INFO)


def _decrypt(client, ciphertext):
    """ Use Google KMS to decrypt the ciphertext """

    if 'GCP_KMS_KEY_ID' not in os.environ:
        logging.error('Error: Missing environment variable: GCP_KMS_KEY_ID')
        return None

    key_id = os.environ['GCP_KMS_KEY_ID']

    keys = client.projects().locations().keyRings().cryptoKeys()

    response = keys.decrypt(
        name=key_id,
        body={"ciphertext": ciphertext},
    ).execute()

    return base64.b64decode(response['plaintext']).decode('utf-8').strip()


def _get_config(filename):
    """ Read the configuration from Cloud Storage """

    try:
        if 'GCS_BUCKET_NAME' not in os.environ:
            logging.error(
                'Error: Missing environment variable: GCS_BUCKET_NAME',
            )
            return None

        bucket_name = os.getenv('GCS_BUCKET_NAME')

        if enable_logging is True:
            logging.info('Reading bucket: %s', bucket_name)

        blob = storage.Client() \
            .get_bucket(bucket_name) \
            .get_blob(filename) \
            .download_as_string()

        return base64.b64encode(blob).decode()

    except Exception as e:
        logging.error(str(e))
        return None


def get_config():
    data = _get_config(CONFIG_PATH)

    kms_client = discovery.build('cloudkms', 'v1', cache_discovery=False)
    decrypted_secret = _decrypt(kms_client, data)

    return json.loads(decrypted_secret)
