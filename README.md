# README

## Local development

```sh
mkvirtualenv soxaas
workon soxaas
pip install -r dev_requirements.txt
```

## Env vars

```bash
# env_vars file
export GCF_REGION=
export GCP_PROJECT_ID=
export BASE_URL=https://$GCF_REGION-$GCP_PROJECT_ID.cloudfunctions.net/
export GCLOUD_TOKEN=$(gcloud auth print-identity-token)
export GOOGLE_APPLICATION_CREDENTIALS=google_credentials.json
```

### `.env.yaml`
```yaml
SECRET_RESOURCE_NAME: projects/<project-id>/locations/global/keyRings/<keyring>/cryptoKeys/<key>
SECRET_API_TOKEN: <encrypted api token>
```


```sh
source env_vars
```

## Tests

### Local tests

**REQUIRES SECRETS**

```sh
./scripts.sh tests
```

### System tests

```sh
./scripts.sh deploy
./scripts.sh system_tests
./scripts.sh destroy
```

## Secrets

1. [Crypto Key](https://console.cloud.google.com/security/kms)

2. Cloud Shell
    * Login
    ```sh
    gcloud alpha cloud-shell ssh
    ```
    * Encrypt a key
    ```sh
    pip3 install google-cloud-kms --user
    python3
    ```

    ```python
    from google.cloud import kms
    import base64

    kms_client = kms.KeyManagementServiceClient()

    resource_name = (
    "projects/<project-id>/" + \
    "locations/global/" + \
    "keyRings/<keyring>/" + \
    "cryptoKeys/<key>/" + \
    "cryptoKeyVersions/1")

    secret = kms_client.encrypt(resource_name, bytes("The chickens are in the hayloft.", "ascii"))
    base64.b64encode(secret.ciphertext) # Encrypted api token
    ```

3. IAM policy
```sh
gcloud kms keys add-iam-policy-binding api_token \
    --location global \
    --keyring <keyring> \
    --role roles/cloudkms.cryptoKeyDecrypter \
    --member serviceAccount:<account>@<project-id>.iam.gserviceaccount.com

# Deploy with env vars
gcloud functions deploy hello_world --env-vars-file app/.env.yaml --runtime python37 --trigger-http --source app/
```

4. Decrypt key
```python
import os
import base64

from google.cloud import kms

def get_secret():
    kms_client = kms.KeyManagementServiceClient()
    return kms_client.decrypt(
        os.environ["SECRET_RESOURCE_NAME"],
        base64.b64decode(os.environ["SECRET_API_TOKEN"]),
    ).plaintext
```