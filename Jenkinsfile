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
        script {
          ant.replace(file: "manifest.jps", token: "GIT_USER", value: "trouduc")
          ant.replace(file: "manifest.jps", token: "GIT_PASSWORD", value: "hahaha")

          sh 'chmod u+x ./deploy-to-jelastic.sh'
          sh "./deploy-to-jelastic.sh $HIDORA_CREDENTIALS_USR $HIDORA_CREDENTIALS_PSW $ENVIRONMENT_NAME"
        }
      }
    }
  }
}
