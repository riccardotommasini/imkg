#!/usr/bin/env bash

# stripped everything down to bare essentials
airflow db upgrade
airflow users create \
  --username "${_AIRFLOW_WWW_USER_USERNAME}" \
  --password "${_AIRFLOW_WWW_USER_PASSWORD}" \
  --firstname admin \
  --lastname admin \
  --email admin@example.org \
  --role Admin
airflow scheduler &
sleep 10
airflow webserver