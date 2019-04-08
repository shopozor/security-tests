pipeline {
  agent {
    docker {
      image 'everpeace/curl-jq'
    }
  } 
  stages {
    stage('Test') {
      environment {
        HIDORA_CREDENTIALS = credentials('hidora-credentials')
        GITHUB_CREDENTIALS = credentials('github-credentials')
        ENVIRONMENT_NAME = "jenkins-test"
      }
      steps {
        sh 'sed -i "s/GIT_USER/$GITHUB_CREDENTIALS_USR/g" manifest.jps'
        sh 'sed -i "s/GIT_PASSWORD/$GITHUB_CREDENTIALS_PSW/g" manifest.jps'
        sh 'chmod u+x ./deploy-to-jelastic.sh'
        sh "./deploy-to-jelastic.sh $HIDORA_CREDENTIALS_USR $HIDORA_CREDENTIALS_PSW $ENVIRONMENT_NAME"
      }
    }
  }
}
