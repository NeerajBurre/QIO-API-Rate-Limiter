pipeline {
    agent any
    
    environment {
        PYTHON_PATH = 'C:\\Users\\neera\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[url: 'https://github.com/NeerajBurre/QIO-API-Rate-Limiter.git']]
                ])
            }
        }

        stage('Run Rate Limiter Demo') {
            steps {
                bat "\"${PYTHON_PATH}\" main.py"
            }
        }
    }
}