pipeline {
    agent any
    environment {
        REPLICA_NUMBER = "3"
    }
    stages {
        stage('Clean') {
            steps {
                script {
                    try {
                        echo 'Removing old image and container'
                        sh '''
                        docker run hello-world
                        docker stop $(docker ps -aq)
                        docker rm $(docker ps -aq)
                        docker rmi -f $(docker images -q)
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
                            sh 'docker build -t 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER .'           
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
                            docker run -d -p 80:80 --name monster-container-$GIT_COMMIT-$BUILD_NUMBER 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER
                            python3 selenium_negative.py         
                            python3 selenium_positive.py                                               
                            docker stop monster-container-$GIT_COMMIT-$BUILD_NUMBER
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
                        docker push 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER
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
                        echo ${env.REPLICA_NUMBER}
                        sh '''
                        sudo aws eks --region us-east-1 update-kubeconfig --name monster-eks-cluster-newest2
			            sed -i "s~image:.*~image: 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER~" monster-deployment.yaml
                        sed -i "s~replicas:.*~replicas: $REPLICA_NUMBER" monster-deployment.yaml                    
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