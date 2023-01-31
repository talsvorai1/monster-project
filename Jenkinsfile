pipeline {
    agent any
    environment {
        PREVIOUS_BUILD = "${BUILD_NUMBER.toInteger() - 1}"
    }

    stages {
        stage('Clean') {
            steps {
                echo 'Removing old image and container'
                sh '''
                docker rm $(docker ps -aq)
                docker rmi -f $(docker images | grep '642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo')
                '''                
            }
        }
        stage('Build') {
            steps {
                echo 'Creating new image and running container'
                sh '''
                cd weather_project
                docker build -t 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$BUILD_NUMBER .
                docker run -d -p 80:8989 --name monster-container-$BUILD_NUMBER 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$BUILD_NUMBER
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing app connectivity'
                sh 'python3 -m unittest connection-unittest.py'
            }
        }
        stage('Upload to ECR') {
            steps {
                echo 'Uploading artifact to ECR'

                echo 'Stoping container'
                sh 'docker stop monster-container-$BUILD_NUMBER'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
