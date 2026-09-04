pipeline {
    agent any
    
    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out latest code from GitHub...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'pip install -r requirements.txt'
            }
        }
        
        stage('Code Testing & Validation') {
            steps {
                echo 'Running basic script validation...'
                bat 'python -m py_compile main.py'
            }
        }
        
        stage('Deploy Backend Service') {
            steps {
                echo 'Executing Rate Limiter Script...'
                bat 'python main.py'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline Execution Completed.'
        }
        success {
            echo 'Build Succeeded Successfully!'
        }
        failure {
            echo 'BUILD FAILED: Check logs above for details.'
        }
    }
}