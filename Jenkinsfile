pipeline {
    agent any
    environment {
        DOCKERHUB_REPO = 'REPLACE_WITH_DOCKERHUB_USERNAME/24mis0364-invoice-system'
        K8S_NAMESPACE = 'default'
    }
    stages {
        stage('1. Source Code Checkout') {
            steps { checkout scm }
        }
        stage('2. Build Application') {
            steps { bat 'python -m pip install -r requirements.txt' }
        }
        stage('3. Run Unit Tests') {
            steps { bat 'python -m pytest -v' }
        }
        stage('4. Build Docker Images') {
            steps {
                bat 'docker build --build-arg APP_VERSION=v1 -t %DOCKERHUB_REPO%:v1 .'
                bat 'docker build --build-arg APP_VERSION=v2 -t %DOCKERHUB_REPO%:v2 .'
                bat 'docker build --build-arg APP_VERSION=v3 -t %DOCKERHUB_REPO%:v3 .'
            }
        }
        stage('5. Push Images to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                    bat 'echo %DH_TOKEN%| docker login -u %DH_USER% --password-stdin'
                    bat 'docker push %DOCKERHUB_REPO%:v1'
                    bat 'docker push %DOCKERHUB_REPO%:v2'
                    bat 'docker push %DOCKERHUB_REPO%:v3'
                }
            }
        }
        stage('6. Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/'
            }
        }
        stage('7. Verify Deployment') {
            steps {
                bat 'kubectl rollout status deployment/invoice-v1'
                bat 'kubectl rollout status deployment/invoice-v2'
                bat 'kubectl rollout status deployment/invoice-v3'
                bat 'kubectl get deployments,services,pods'
            }
        }
    }
    post {
        always { bat 'docker image ls' }
        success { echo 'Invoice System pipeline completed successfully.' }
        failure { echo 'Pipeline failed. Review the stage and console output.' }
    }
}