pipeline {
  agent any

  environment {
    REMOTE_HOST = "ubuntu@your-server-ip"
    REMOTE_DIR = "/home/ubuntu/real-estate-llm"
  }

  stages {

    stage('Build Docker Locally (optional)') {
      steps {
        sh 'docker build -t real-estate-langgraph:latest .'
      }
    }

    stage('Send Files to Remote') {
      steps {
        sshagent(credentials: ['jenkins-ssh-key']) {
          sh """
            ssh -o StrictHostKeyChecking=no $REMOTE_HOST '
              mkdir -p $REMOTE_DIR
            '
            scp -r * $REMOTE_HOST:$REMOTE_DIR
          """
        }
      }
    }

    stage('Deploy on Remote Server') {
      steps {
        sshagent(credentials: ['jenkins-ssh-key']) {
          sh """
            ssh $REMOTE_HOST '
              cd $REMOTE_DIR &&
              docker-compose down &&
              docker-compose up -d --build
            '
          """
        }
      }
    }
  }
}
