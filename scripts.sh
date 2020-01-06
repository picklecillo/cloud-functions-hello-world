#!/bin/sh

case $1 in

  init_workspace)
    mkvirtualenv soxaas
    workon soxaas
    pip install -r app/dev_requirements.txt
    pip install -r app/requirements.txt
  ;;

  tests)
    pytest app/test.py -v
    ;;

  api_tests)
    pytest app/test_api.py -v
    ;;

  system_tests)
    pytest app/system_test.py -v
    ;;

  deploy)
    gcloud functions deploy hello_world --env-vars-file app/.env.yaml --runtime python37 --trigger-http --source app/
    ;;

  destroy)
    gcloud functions delete hello_world
    ;;

  *)
    echo -n "unknown cmd"
    ;;
esac
