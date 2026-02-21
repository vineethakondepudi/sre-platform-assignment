pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Building image...'
      }
    }
    stage('Push') {
      steps {
        echo 'Pushing to ECR...'
      }
    }
    stage('Deploy') {
      steps {
        echo 'Deploying to Kubernetes...'
      }
    }
  }
}
