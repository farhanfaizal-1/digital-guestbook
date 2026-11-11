
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Project') {
            steps {
                sh 'ls -la'
                sh 'docker compose config'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker rm -f guestbook-backend guestbook-frontend || true
                    docker compose up -d
                '''
            }
        }

        stage('Check Containers') {
            steps {
                sh 'docker compose ps'
            }
        }

        stage('Test Application') {
            steps {
                sh '''
                    sleep 5

                    curl -fsS http://localhost:8080/api/messages

                    curl -fsS -X POST \
                    http://localhost:8080/api/messages \
                    -H "Content-Type: application/json" \
                    -d '{"name":"Jenkins Test","institution":"Universitas Telkom","purpose":"Pengujian CI/CD"}'
                '''
            }
        }
    }
}
