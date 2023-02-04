pipeline {
    agent any
    stages {
        stage('Check branch') {
            steps {
                echo "BRANCH_NAME = ${env.GIT_BRANCH}"
            }
        }
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
                    }
                }                    
            }
        }
        stage('Build') {         
            steps {
                script {
                    try {
                        echo 'Creating new image, running and stopping container'
                        sh '''
                        cd weather_project
                        docker build -t 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER .
                        docker run -d -p 80:443 --name monster-container-$GIT_COMMIT-$BUILD_NUMBER 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER
                        docker stop monster-container-$GIT_COMMIT-$BUILD_NUMBER                
                        '''
                    } catch (error) {
                        slackSend channel: "devops-alerts", message: "Build Failed in Build stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
                    } 
                }       
            }
        }
        stage('Test') {     
            steps {
                script {
                    try {
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
                    } catch (error) {
                        slackSend channel: "devops-alerts", message: "Build Failed in Test stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
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
                    }
                }    
            }    
        }
        stage('Deployment') {
            when {
                expression { return ${env.GIT_BRANCH} == 'origin/main' }
            }            
            steps {
                script {
                    try {
                        echo 'Connecting via ssh to master node'
                        echo 'Pulling and deploying Artifact'
		                sshagent(['monster-deploy-cred']) {
                        sh '''
	                    ssh -o StrictHostKeyChecking=no -l ubuntu 3.226.109.188 << EOF
			            sed -i "s~image:.*~image: 642341975645.dkr.ecr.us-east-1.amazonaws.com/monster-image-repo:$GIT_COMMIT-$BUILD_NUMBER~" monster-deployment.yaml                    
                        kubectl apply -f monster-deployment.yaml
                        '''
		                }
		            } catch (error) {
                        slackSend channel: "devops-alerts", message: "Build Failed in Deployment stage: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
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