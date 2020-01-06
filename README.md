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
```

```sh
source env_vars
```

### Local tests

```sh
./scripts.sh tests
```

### System tests

```sh
./scripts.sh deploy
./scripts.sh system_tests
./scripts.sh destroy
```

