pipeline{
    agent any
    environment{
            DOCKER_IMAGE='23bcd2-assignment5:latest'
            DOCKERHUB_USERNAME='muzankibetsuji'
            EC2_USER='ubuntu'
            EC2_IP='16.112.159.37'

    }
    stages{
        stage('Checkout SCM'){
            steps{
                checkout scm
            }
        }

        stage('Creating Docker Image') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop 23bcd2-slangdb || true
                docker rm 23bcd2-slangdb || true
                docker run -d -p 3000:3000 -v assignment5:/app --name 23bcd2-slangdb ${DOCKER_IMAGE}
                '''
            }
        }

        stage('Tagging Docker Image') {
            steps {
                echo 'Tagging Docker Image...'
                sh 'docker tag ${DOCKER_IMAGE} ${DOCKERHUB_USERNAME}/${DOCKER_IMAGE}'
            }
        }

        stage('Pushing Docker Image') {
            steps {
                // you fucking need the credentials, whore!
                withCredentials([string(credentialsId: 'dockerhub-token', variable:'DOCKER_TOKEN')]){
                    echo 'Pushing Docker Image...'
                    sh 'echo "$DOCKER_TOKEN" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin'
                    sh 'docker push ${DOCKERHUB_USERNAME}/${DOCKER_IMAGE}'
                }
            }
        }

        stage('Deploy on AWS EC2'){
            steps{
                sshagent([credentials:['ec2-pem-file']]){
                    sh """
                        ssh -o StrictHostKeyChecking=no -o ConnectTimeout=15 ${EC2_USER}@${EC2_IP} "
                            echo "Connected to EC2"
                            docker --version
                            exit
                        "
                    """
                }
            }
        }
    }
}