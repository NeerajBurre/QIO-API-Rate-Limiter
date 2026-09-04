pipeline {
    agent any
    
    environment {
        // Full path to your Python executable
        PYTHON_EXE = 'C:\\Users\\neera\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }
    
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
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
            }
        }
        
        stage('Code Testing & Validation') {
            steps {
                echo 'Running basic script validation...'
                bat '"%PYTHON_EXE%" -m py_compile main.py'
            }
        }
        
        stage('Deploy Backend Service') {
            steps {
                echo 'Executing Rate Limiter Script...'
                bat '"%PYTHON_EXE%" main.py'
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