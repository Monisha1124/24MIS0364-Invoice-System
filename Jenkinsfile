
pipeline {
    agent any

    environment {
        IMAGE = 'monisha1124/24mis0364-invoice-system'
    }

    stages {
        stage('1. Source Code Checkout') {
            steps {
                echo 'Source code checked out from GitHub'
                bat 'git rev-parse --short HEAD'
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

       stage('5. Push Images to DockerHub') {
            steps {
        echo 'Docker images built locally. DockerHub push temporarily skipped due to authentication issue.'
        bat 'docker image ls'
    }
}

        stage('6. Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/invoice-v1.yaml'
                bat 'kubectl apply -f k8s/invoice-v2.yaml'
                bat 'kubectl apply -f k8s/invoice-v3.yaml'
            }
        }

        stage('7. Verify Deployment') {
            steps {
                bat 'kubectl rollout status deployment/invoice-v1 --timeout=120s'
                bat 'kubectl rollout status deployment/invoice-v2 --timeout=120s'
                bat 'kubectl rollout status deployment/invoice-v3 --timeout=120s'
                bat 'kubectl get deployments'
                bat 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'Invoice System CI/CD Pipeline Completed Successfully!'
        }
        failure {
            echo 'Pipeline failed. Review the stage and console output.'
            bat 'docker image ls'
        }
    }
}
