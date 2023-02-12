pipeline {
    agent any
    environment {
        REPLICA_NUMBER = '2'
        TAG = "${env.GIT_COMMIT}-${env.BUILD_NUMBER}"
        ECR_REPO = '642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo'
    }
    stages {
        stage('Build and Clean') {
            steps {
                dir('weather_project') {
                    script {
                        try {
                            echo 'Creating new image and container'
                            sh '''
                            docker build -t $ECR_REPO:$TAG .
                            current_containers=$(docker ps -aq)
                            if [ -n "$current_containers" ]; then
                                docker stop $current_containers
                            fi    
                            docker run -d -p 80:80 --name monster-container-$TAG $ECR_REPO:$TAG
                            '''
                            echo 'Removing images and containers prior to current'
                            sh '''
                            previous_containers=$(docker ps -aq --filter "before=monster-container-$TAG")
                            if [ -n "$previous_containers" ]; then
                                docker rm $previous_containers
                            fi

                            previous_images=$(docker images -q --filter "before=$ECR_REPO:$TAG" --filter "since=python:3.8-alpine")
                            if [ -n "$previous_images" ]; then
                                docker rmi -f $previous_images
                            fi
                            '''
                        } catch (error) {
                            slackSend channel: "devops-alerts", message: "Build Failed in Clean stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
                            currentBuild.result = 'FAILURE'
                            error 'Build failed in Build and Clean stage'
                        }
                    }    
                }                    
            }
        }
        stage('Test') {     
            steps {
                dir('weather_project') {
                    script {
                        try {
                            
                            echo 'Testing app connectivity with unittest'
                            sh '''
                            python3 -m unittest connection_unittest.py
                            '''
                            echo 'Testing functionality via positive and negative selenium tests'
                            sh '''
                            python3 selenium_negative.py         
                            python3 selenium_positive.py                                               
                            docker stop monster-container-$TAG
                            ''' 
                        } catch (error) {
                            slackSend channel: "devops-alerts", message: "Build Failed in Test stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
                            currentBuild.result = 'FAILURE'
                            error 'Build failed in Test stage'
                        }
                    }
                }
            }     
        }    
        stage('Push to ECR') {
            steps {
                script {
                    try {
                        echo 'Uploading artifact to ECR'
                        sh '''
                        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 642341975645.dkr.ecr.us-east-1.amazonaws.com
                        docker push $ECR_REPO:$TAG
                        '''
                    } catch (error) {
                        slackSend channel: "devops-alerts", message: "Build Failed in Push stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
                        currentBuild.result = 'FAILURE'
                        error 'Build failed in Push stage'
                    }
                }    
            }    
        }
        stage('Deployment') {
            when {
                expression { return "${env.GIT_BRANCH}" == "origin/main" }
            }            
            steps {
                script {
                    try {
                        echo 'Updating image'
                        sh '''
                        sudo aws eks --region us-east-1 update-kubeconfig --name monster-eks-cluster-newest3
                        cp monster-deployment.yaml monster-deployment-backup.yaml
			            sed -i "s~image:.*~image: $ECR_REPO:$TAG~" monster-deployment.yaml
                        sed -i "s/replicas:.*/replicas: $REPLICA_NUMBER/g" monster-deployment.yaml       
                        kubectl apply -f monster-deployment.yaml
                        kubectl apply -f monster-service.yaml
                        '''
		            } catch (error) {
                        slackSend channel: "devops-alerts", message: "Build Failed in Deployment stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
                        currentBuild.result = 'FAILURE'
                        error 'Build failed in Deployment stage'
                    }
                }    
            }    
        }
    }    
    post {
	    success {
            slackSend channel: "succeeded-build", message: "Build Successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
	    }
    }    
}