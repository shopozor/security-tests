CONTENT_TYPE="Content-Type: application/x-www-form-urlencoded; charset=UTF-8;"
USER_AGENT="Mozilla/4.73 [en] (X11; U; Linux 2.2.15 i686)"

TIME_OUT_IN_SECONDS=1800
TIMER_DELTA_IN_SECONDS=5

getCommandResult() {
  local command=$1
  echo $(echo $command | jq '.result')
}

exitOnFail() {
  local command=$1
  local result=$(getCommandResult $command)
  if [[ "$result" != "0" ]] ; then
    echo "Following command failed with result $result: $command" >&2
    exit 1
  fi
}

getSession() {
  local login=$1
  local password=$2
  local hosterUrl=$3
  echo "Signing in..." >&2
  local cmd=$(curl -k -H "${CONTENT_TYPE}" -A "${USER_AGENT}"  -X POST \
    -fsS "$hosterUrl/1.0/users/authentication/rest/signin" -d "login=$login&password=$password");
  exitOnFail $cmd
  echo "Signed in" >&2
  echo $(jq '.session' <<< $cmd |  sed 's/\"//g')
}

getEnvs() {
  local session=$1
  echo "Getting environments..." >&2
  local cmd=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/getenvs -d "appid=${APPID}&session=${session}")
#  exitOnFail $cmd
  echo "Got environments" >&2
  echo $cmd
}

startEnv() {
  local session=$1
  local envName=$2
  echo "Starting up environment <$envName>..." >&2
  local cmd=$(curl -k \
    -H "${CONTENT_TYPE}" \
    -A "${USER_AGENT}" \
    -X POST \
    -fsS ${HOSTER_URL}/1.0/environment/control/rest/startenv -d "session=${session}&envName=${envName}")
  exitOnFail $cmd
  echo "Environment <$envName> started" >&2
}

startEnvIfNecessary() {
  local session=$1
  local envName=$2
  local envs=$3
  local status=$(echo $envs | jq ".infos[] | select(.env.envName==\"$envName\") | .env.status")
  if [ "$status" != "1" ] ; then
    startEnv $session "$envName"
  fi
}

waitUntilEnvIsRunning () {
  local graphqlEndpoint=$1

  START_TIME=`date +%s`
  while [[ $status -ne 200 ]] ; do
      status=$(curl -H "Content-Type: application/json" \
          -w "%{http_code}" \
          -d '{ "query": "query { me { id } }", "variables": "{}" }' \
          -so /dev/null \
          -X POST \
          $graphqlEndpoint)
      CURRENT_TIME=`date +%s`
      RUNTIME=$((CURRENT_TIME - START_TIME))
      if [ $RUNTIME -ge $TIME_OUT_IN_SECONDS ] ; then
        echo "Waking up environment timed out"
        exit 1
      fi
      sleep $TIMER_DELTA_IN_SECONDS
  done
}