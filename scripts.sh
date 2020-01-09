#!/bin/bash

case $1 in

  # Local
  init_workspace)
    pip install -r app/app/requirements.txt
    pip install -r app/app/dev_requirements.txt
    pip install -e app/
  ;;

  # Tests
  function_tests)
    pytest app/tests/test_function.py -vs
    ;;

  api_tests)
    pytest app/tests/test_api.py -vs
    ;;

  system_tests)
    pytest app/tests/system_test.py -vs
    ;;

  all_tests)
    pytest --cov=function --cov-report=html --cov-report term app/tests/ -vs
    ;;

  serve_coverage)
    cd htmlcov
    python -m http.server 8001
    ;;

  # Deploy
  gcp_login)
    gcloud auth activate-service-account $GCP_SA \
      --key-file=google_credentials.json \
      --project=$GCP_PROJECT_ID
    ;;


  deploy)
    gcloud functions deploy hello_world \
     --env-vars-file app/.env.yaml \
     --runtime python37 \
     --trigger-http \
     --source app/function/ \
     --service-account $GCP_SA
    ;;

  destroy)
    gcloud functions delete hello_world
    ;;

  # KMS
  kms_setup_keyring)
    gcloud kms keyrings create $GCP_KMS_KEYRING \
      --location $GCP_LOCATION

    gcloud kms keys create $GCP_KMS_KEYNAME \
      --keyring $GCP_KMS_KEYRING \
      --location $GCP_LOCATION \
      --purpose encryption
    ;;

  kms_encrypt_config)
    gcloud kms encrypt \
      --keyring=$GCP_KMS_KEYRING \
      --key=$GCP_KMS_KEYNAME \
      --location $GCP_LOCATION \
      --plaintext-file=config.json \
      --ciphertext-file=config.enc
    ;;

  kms_setup_policy)
    gcloud kms keys add-iam-policy-binding $GCP_KMS_KEYNAME \
      --location $GCP_LOCATION \
      --keyring $GCP_KMS_KEYRING \
      --member serviceAccount:$GCP_SA \
      --role $GCP_KMS_ROLE
    ;;

  gcs_setup_bucket)
    gsutil mb gs://$GCS_BUCKET_NAME
    gsutil defacl set private gs://$GCS_BUCKET_NAME
    gsutil versioning set on gs://$GCS_BUCKET_NAME
    ;;

  gcs_copy_config)
    gsutil -h "Content-Type: application/octet-stream" cp config.enc gs://$GCS_BUCKET_NAME/config.enc

    gsutil iam ch serviceAccount:$GCP_SA:$GCS_BUCKET_ROLE gs://$GCS_BUCKET_NAME/
    gsutil iam ch serviceAccount:$GCP_SA:$GCS_OBJECT_ROLE gs://$GCS_BUCKET_NAME/config.enc

    # this command will return an error on an empty bucket
    gsutil acl set private gs://$GCS_BUCKET_NAME/config.enc
    gsutil acl set private gs://$GCS_BUCKET_NAME/config.enc

    ;;

  *)
    echo -n "unknown cmd"
    ;;
esac
