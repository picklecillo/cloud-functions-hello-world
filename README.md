 # README

## Local development

```sh
mkvirtualenv soxaas
./scripts.sh init_workspace
```

## `env_vars`

```bash
# env_vars file
export GCF_REGION=
export GCP_PROJECT_ID=
export GOOGLE_CLOUD_PROJECT=$GCP_PROJECT_ID
export GCP_LOCATION=global

export GCP_KMS_KEYRING=
export GCP_KMS_KEYNAME=
export GCP_KMS_ROLE=roles/cloudkms.cryptoKeyDecrypter
export GCP_KMS_KEY_ID=projects/$GCP_PROJECT_ID/locations/$GCP_LOCATION/keyRings/$GCP_KMS_KEYRING/cryptoKeys/$GCP_KMS_KEYNAME

export GCP_SA_NAME=
export GCP_SA=$GCP_SA_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com

export GCS_BUCKET_PREFIX=
export GCS_BUCKET_NAME=$GCP_PROJECT_ID-$GCS_BUCKET_PREFIX
export GCS_BUCKET_ROLE=legacyBucketReader
export GCS_OBJECT_ROLE=legacyObjectReader

export BASE_URL=https://$GCF_REGION-$GCP_PROJECT_ID.cloudfunctions.net/

export GOOGLE_APPLICATION_CREDENTIALS=
```

### `app/.env.yaml`
```yaml
GCS_BUCKET_NAME:
GCP_KMS_KEY_ID:

```


```sh
source env_vars
```

## Tests

**TESTS REQUIRE SECRETS**

### Local tests

```sh
./scripts.sh tests
```

### Integration Tests

```sh
./scripts.sh deploy
# > ./scripts.sh deploy
# Allow unauthenticated invocations of new function [hello_world]?
# (y/N)?  N
./scripts.sh system_tests
./scripts.sh destroy
```

### API Tests
```sh
./scripts.sh api_tests
```

### All tests
```sh
./scripts.sh all_tests
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

## Scripts

Required apis:
* `cloudkms.googleapis.com`
* `cloudfunctions.googleapis.com`
* `cloudresourcemanager.googleapis.com/`

Required Roles:
* `Cloud Functions Developer`
* `Service Account User`

Required permissions for service account:
* `cloudkms.keyRings.create`
* `cloudkms.cryptoKeys.create`
* `cloudkms.cryptoKeyVersions.useToEncrypt`
* `cloudkms.cryptoKeys.getIamPolicy`
* `storage.objects.get`