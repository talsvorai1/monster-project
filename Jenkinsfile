pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Creating new image'
                sh '''
                cd weather_project
                docker build -t 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$BUILD_NUMBER .
                docker run -d -p 80:8989 --name monster-container-$BUILD_NUMBER 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$BUILD_NUMBER
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Upload to ECR') {
            steps {
                echo 'Pruning old containers and images'
                sh '''
                docker rm -f $(docker ps -aq)
                docker rmi -f $(docker images -aq)
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
