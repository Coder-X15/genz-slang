pipeline{
    agent any
    stages{
        stage('Checkout SCM'){
            steps{
                checkout scm
            }
        }
        stage('Creating Docker Image') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t 23bcd2-assignment5:latest .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop 23bcd2-slangdb || true
                docker rm 23bcd2-slangdb || true
                docker run -d -p 5000:5000 -v assignment5:/app --name 23bcd2-slangdb 23bcd2-assignment5:latest
                '''
            }
        }

        stage('Tagging Docker Image') {
            steps {
                echo 'Tagging Docker Image...'
                sh 'docker tag 23bcd2-assignment5:latest muzankibetsuji/23bcd2-assignment5:latest'
            }
        }

        stage('Pushing Docker Image') {
            steps {
                // you fucking need the credentials, whore!
                withCredentials([string(credentialsId: 'dockerhub-token', variable:'DOCKER_TOKEN')]){
                    echo 'Pushing Docker Image...'
                    sh 'echo "$DOCKER_TOKEN" | docker login -u muzankibetsuji --password-stdin'
                    sh 'docker push muzankibetsuji/23bcd2-assignment5:latest'
                }
            }
        }
    }
}