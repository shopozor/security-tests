#!/bin/bash

if [ $# -lt 5 ] ; then
  echo "Usage: $0 hosterUrl appId login password envName"
  exit 0
fi

. scripts/helpers.sh

HOSTER_URL=$1
APPID=$2

SESSION=$(getSession $3 $4 ${HOSTER_URL})
ENV_NAME=$5

wakeUp() {
  ENVS=$(getEnvs $SESSION)

  startEnvIfNecessary $SESSION "${ENV_NAME}" "$ENVS"
  ENDPOINT="http://${ENV_NAME}.hidora.com/graphql/"
  waitUntilEnvIsRunning "$ENDPOINT"

  exit 0
}

wakeUp
