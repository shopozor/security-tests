pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  }
  environment {
    // REPORTS_FOLDER = "junit-reports"
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
    stage('Security Tests') {
        steps {
            withEnv(["HOME=$WORKSPACE"]) {
                sh ". $VENV/bin/activate && cd tests/backend && pytest --domain $DOMAIN --graphql-endpoint graphql/ -ra --junitxml=backend-tests.xml"
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