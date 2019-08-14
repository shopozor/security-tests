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

wasEnvCreated() {
  echo "envName = $2" >&2
  local envs=$1
  local envName=$2
  echo "Check if environment <$envName> exists..." >&2
  local envExists=$(echo $envs | jq '[.infos[].env.envName]' | jq "index(\"$envName\")")
  echo "Existence of environment <$envName> checked" >&2
  echo $envExists
}

wakeUp() {
  ENVS=$(getEnvs $SESSION)
  CREATED=$(wasEnvCreated "$ENVS" "${ENV_NAME}")

  # if [ "${CREATED}" == "null" ]; then
  #   echo "Environment $envName does not exist!"
  #   exit 1
  # else
    startEnvIfNecessary $SESSION "${ENV_NAME}" "$ENVS"
    waitUntilEnvIsRunning $SESSION "${ENV_NAME}"
  # fi

  exit 0
}

wakeUp
