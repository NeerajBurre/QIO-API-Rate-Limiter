pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out latest code from GitHub...'
                checkout scm
                
                echo '================ GIT CHANGES DETECTED ================'
                sh 'git log -1 --stat'
                echo '======================================================'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Creating Python virtual environment & installing packages...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Verify Redis Server') {
            steps {
                echo 'Testing Redis service connection...'
                sh 'redis-cli ping || (echo "Redis server is offline!" && exit 1)'
            }
        }

        stage('Code Testing & Validation') {
            steps {
                echo 'Compiling Python scripts...'
                sh '''
                    . venv/bin/activate
                    python3 -m py_compile main.py
                '''
            }
        }

        stage('Deploy Backend Service') {
            steps {
                echo 'Deploying FastAPI application...'
                sh '''
                    . venv/bin/activate
                    pkill -f uvicorn || true
                    nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
                    sleep 2
                    curl -s http://localhost:8000/api || true
                '''
            }
        }
    }

    post {
        success {
            echo '=================================================='
            echo ' BUILD SUCCESSFUL: CI/CD Pipeline Execution Done '
            echo '=================================================='
        }
        failure {
            echo ' BUILD FAILED: Check app.log or console logs for errors.'
        }
    }
}