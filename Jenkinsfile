pipeline {
    agent any
    environment {
        REPLICA_NUMBER = '2'
        TAG = "${env.GIT_COMMIT}-${env.BUILD_NUMBER}"
        ECR_REPO = '642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo'
    }
    stages {
        stage('Clean') {
            steps {
                script {
                    try {
                        echo 'Removing old images and containers if exist (-n meaning non-empty test)'
                        sh '''
                        containers_var=$(docker ps -aq)
                        if [ -n "$containers_var" ]; then
                            docker stop $containers_var
                            docker rm $containers_var
                        fi

                        images_var=$(docker images -q)
                        if [ -n "$images_var" ]; then
                            docker rmi -f $images_var
                        fi
                        '''
                    } catch (error) {
                        slackSend channel: "devops-alerts", message: "Build Failed in Clean stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
                        currentBuild.result = 'FAILURE'
                        error 'Build failed in Clean stage'
                    }
                }                    
            }
        }
        stage('Build') {         
            steps {
                dir('weather_project') {
                    script {
                        try {
                            echo 'Creating new image, running and stopping container'
                            sh 'docker build -t $ECR_REPO:$TAG .'           
                        } catch (error) {
                            slackSend channel: "devops-alerts", message: "Build Failed in Build stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
                            currentBuild.result = 'FAILURE'
                            error 'Build failed in Build stage'                            
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
                            docker run -d -p 80:80 --name monster-container-$TAG $ECR_REPO:$TAG
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
                        sudo aws eks --region us-east-1 update-kubeconfig --name monster-eks-cluster-newest2
                        cp monster-deployment.yaml monster-deployment-backup.yaml
			            sed -i "s~image:.*~image: $ECR_REPO:$TAG~" monster-deployment.yaml
                        sed -i "s/replicas:.*/replicas: $REPLICA_NUMBER/g" monster-deployment.yaml       
                        kubectl apply -f monster-deployment.yaml
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