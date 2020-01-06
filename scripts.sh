#!/bin/bash

case $1 in

  init_workspace)
    pip install -r app/app/dev_requirements.txt
    cd app/
    pip install .
  ;;

  tests)
    pytest app/tests/test.py -v
    ;;

  api_tests)
    pytest app/tests/test_api.py -v
    ;;

  system_tests)
    pytest app/tests/system_test.py -v
    ;;

  all_tests)
    pytest app/tests/ -v
    ;;

  deploy)
    gcloud functions deploy hello_world --env-vars-file app/.env.yaml --runtime python37 --trigger-http --source app/app/
    ;;

  destroy)
    gcloud functions delete hello_world
    ;;

  *)
    echo -n "unknown cmd"
    ;;
esac
