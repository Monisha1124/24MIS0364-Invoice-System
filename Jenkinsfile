
pipeline {
    agent any

    environment {
        IMAGE = 'monisha1124/24mis0364-invoice-system'
    }

    stages {
        stage('1. Source Code Checkout') {
            steps {
                bat 'git rev-parse --short HEAD'
                echo 'Git checkout successful'
            }
        }

        stage('2. Build Application') {
            steps {
                bat 'docker build --build-arg APP_VERSION=v3 -t invoice-system-test .'
            }
        }

        stage('3. Run Unit Tests') {
            steps {
                bat 'docker run --rm invoice-system-test python -m pytest -q'
            }
        }

        stage('4. Build Docker Images') {
            steps {
                bat 'docker build --build-arg APP_VERSION=v1 -t %IMAGE%:v1 .'
                bat 'docker build --build-arg APP_VERSION=v2 -t %IMAGE%:v2 .'
                bat 'docker build --build-arg APP_VERSION=v3 -t %IMAGE%:v3 .'
            }
        }

        stage('5. Docker Image Verification') {
            steps {
                bat 'docker image inspect %IMAGE%:v1'
                bat 'docker image inspect %IMAGE%:v2'
                bat 'docker image inspect %IMAGE%:v3'
            }
        }

        stage('6. Kubernetes Deployment Verification') {
            steps {
                bat 'kubectl get deployments'
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }

        stage('7. Final Verification') {
            steps {
                bat 'kubectl rollout status deployment/invoice-v1 --timeout=120s'
                bat 'kubectl rollout status deployment/invoice-v2 --timeout=120s'
                bat 'kubectl rollout status deployment/invoice-v3 --timeout=120s'
                echo 'Invoice System verification completed'
            }
        }
    }

    post {
        success {
            echo 'INVOICE SYSTEM PIPELINE COMPLETED SUCCESSFULLY'
        }
        failure {
            echo 'Pipeline failed. Check the stage error.'
        }
    }
}

