pipeline {
    agent any
    
    environment {
        PYTHON_PATH = 'C:\\Users\\neera\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {
        stage('Clean & Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Run Rate Limiter Demo') {
            steps {
                bat "\"${PYTHON_PATH}\" main.py"
            }
        }
    }
}