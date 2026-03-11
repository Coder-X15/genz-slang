pipeline{
    agent any
    stages{
        stage('Checkout'){
            steps{
                echo 'Checking out the code...'
                checkout scm
            }
        }
        stage('Build'){
            steps{
                echo 'Building the application...'
                sh 'docker build -t flask-webapp .'
            }
        }
        stage('Test'){
            steps{
                echo 'Testing the application...'
                // Add your testing commands here
            }
        }
        stage('Deploy'){
            steps{
                echo 'Deploying the application...'
                // Add your deployment commands here
            }
        }
    }
}