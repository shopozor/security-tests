pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  }
  environment {
    JELASTIC_APP_CREDENTIALS = credentials('jelastic-app-credentials')
    JELASTIC_CREDENTIALS = credentials('jelastic-credentials')
    VENV = 'venv'
  }
  stages {
    stage('Virtual Environment Installation') {
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "pip install virtualenv --user"
          sh "$WORKSPACE/.local/bin/virtualenv $VENV"
          sh ". $VENV/bin/activate"
          sh ". $VENV/bin/activate && pip install -r tests/requirements.txt"
        }
      }
    }
    stage('Wake up Jelastic environment') {
        steps {
            script {
                SCRIPT_TO_RUN = './scripts/wake-up-env.sh'
                sh ". $VENV/bin/activate && python venv/lib/python3.7/site-packages/dos2unix.py ./scripts/helpers.sh ./scripts/helpers.sh"
                sh ". $VENV/bin/activate && python venv/lib/python3.7/site-packages/dos2unix.py $SCRIPT_TO_RUN $SCRIPT_TO_RUN"
                sh "chmod u+x $SCRIPT_TO_RUN"
                sh "$SCRIPT_TO_RUN $JELASTIC_APP_CREDENTIALS_USR $JELASTIC_APP_CREDENTIALS_PSW $JELASTIC_CREDENTIALS_USR $JELASTIC_CREDENTIALS_PSW $HIDORA_DOMAIN"
            }
        }
    }
    stage('Security Tests') {
        steps {
            withEnv(["HOME=$WORKSPACE"]) {
                sh ". $VENV/bin/activate && cd tests/backend && pytest --domain http://${HIDORA_DOMAIN}.hidora.com --graphql-endpoint graphql/ -ra --junitxml=backend-tests.xml"
            }
        }
    }
  }
  post {
    always {
      script {
         junit "**/*.xml"
      }
    }
  }
}