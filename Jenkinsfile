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
                docker rmi $(docker images '642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo' -a -q)
                '''                
            }
        }
        stage('Build') {
            steps {
                echo 'Creating new image, running and stopping container'
                sh '''
                cd weather_project
                docker build -t 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$BUILD_NUMBER .
                docker run -d -p 80:8989 --name monster-container-$BUILD_NUMBER 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$BUILD_NUMBER
                docker stop monster-container-$BUILD_NUMBER                
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing app connectivity'
                sh 'python3 -m unittest Testing_Reachability.py'
            }
        }
        stage('Upload to ECR') {
            steps {
                echo 'Uploading artifact to ECR'


            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
