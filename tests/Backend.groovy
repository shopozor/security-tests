pipeline {
  agent {
    docker {
      image 'softozor/shopozor-security-tests:v0.0.8'
    }
  }
  environment {
    JELASTIC_APP_CREDENTIALS = credentials('jelastic-app-credentials')
    JELASTIC_CREDENTIALS = credentials('jelastic-credentials')
  }
  stages {
    stage('Wake up Jelastic environment') {
        steps {
            script {
                SCRIPT_TO_RUN = '/app/scripts/wake-up-env.sh'
                sh "$SCRIPT_TO_RUN $JELASTIC_APP_CREDENTIALS_USR $JELASTIC_APP_CREDENTIALS_PSW $JELASTIC_CREDENTIALS_USR $JELASTIC_CREDENTIALS_PSW $HIDORA_DOMAIN"
            }
        }
    }
    stage('Security Tests') {
        environment {
          PYTHONPATH = "$PYTHONPATH:$WORKSPACE/tests/common"
        }    
        steps {
            withEnv(["HOME=$WORKSPACE"]) {
                sh "cd tests/backend && pytest --domain http://${HIDORA_DOMAIN}.hidora.com --graphql-endpoint graphql/ -ra --junitxml=backend-tests.xml"
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



