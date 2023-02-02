pipeline {
    agent any
    
    stages {
        stage('Clean') {
            steps {
                echo 'Removing old image and container'
                sh '''
                docker run hello-world
                docker stop $(docker ps -aq)
                docker rm $(docker ps -aq)
                docker rmi -f $(docker images -q)
                '''                
            }
        }
        stage('Build') {
            steps {
                echo 'Creating new image, running and stopping container'
                sh '''
                cd weather_project
                docker build -t 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER .
                docker run -d -p 80:8989 --name monster-container-$GIT_COMMIT-$BUILD_NUMBER 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER
                docker stop monster-container-$GIT_COMMIT-$BUILD_NUMBER                
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing app connectivity with unittest'
                sh '''
                cd weather_project
                python3 -m unittest connection_unittest.py
                '''
                echo 'Testing funcionallity via positive and negative selenium tests'
                sh '''
                cd weather_project
                docker start monster-container-$GIT_COMMIT-$BUILD_NUMBER 
                python3 selenium_negative.py 
                python3 selenium_positive.py 
                docker stop monster-container-$GIT_COMMIT-$BUILD_NUMBER 
                '''
            }
        }    
        stage('Upload to ECR') {
            steps {
                echo 'Uploading artifact to ECR'
                sh '''
                docker push 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER
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