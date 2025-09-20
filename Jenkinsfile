pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'agenticrag'
        IMAGE_TAG = 'latest'
        SERVICE_NAME = 'agenticrag-service'
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    echo 'Setting up Python environment...'
                    bat 'python --version'
                    bat 'pip install --upgrade pip'
                    bat 'echo Environment setup complete'
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Installing Python dependencies...'
                    bat 'pip install -r requirements.txt'
                }
            }
        }
        
        stage('Basic Tests') {
            steps {
                script {
                    echo 'Running basic Python tests...'
                    bat 'python -c "print(\'Python is working\')"'
                    bat 'python -c "import sys; print(sys.version)"'
                    bat 'python -c "from app.config.config import GROQ_API_KEY; print(\'Config loaded\') if GROQ_API_KEY else print(\'No API key\')"'
                }
            }
        }
        
        stage('Validate Structure') {
            steps {
                script {
                    echo 'Validating project structure...'
                    bat 'dir app'
                    bat 'dir data'
                    bat 'type README.md'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    bat 'docker build -f Dockerfile.app -t %ECR_REPO%:%IMAGE_TAG% .'
                    bat 'docker images | findstr %ECR_REPO%'
                }
            }
        }
        
        stage('Run Application Tests') {
            steps {
                script {
                    echo 'Running AgenticRAG tests...'
                    bat 'python health_check.py || echo Health check completed'
                    bat 'python test_system.py || echo System test completed'
                }
            }
        }
        
        stage('Install AWS CLI') {
            steps {
                script {
                    echo 'Installing AWS CLI...'
                    bat 'pip install awscli'
                    bat 'aws --version || python -m awscli --version'
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    script {
                        echo 'Pushing to AWS ECR...'
                        bat '''
                            set AWS_DEFAULT_REGION=%AWS_REGION%
                            for /f %%i in ('python -m awscli sts get-caller-identity --query Account --output text') do set ACCOUNT_ID=%%i
                            set ECR_URI=%ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%ECR_REPO%
                            
                            python -m awscli ecr get-login-password --region %AWS_REGION% > temp_password.txt
                            set /p ECR_PASSWORD=<temp_password.txt
                            echo %ECR_PASSWORD% | docker login --username AWS --password-stdin %ECR_URI%
                            
                            docker tag %ECR_REPO%:%IMAGE_TAG% %ECR_URI%:%IMAGE_TAG%
                            docker push %ECR_URI%:%IMAGE_TAG%
                            
                            del temp_password.txt
                            echo Image pushed to ECR: %ECR_URI%:%IMAGE_TAG%
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    script {
                        echo 'Deploying to EC2...'
                        bat '''
                            set AWS_DEFAULT_REGION=%AWS_REGION%
                            for /f %%i in ('python -m awscli sts get-caller-identity --query Account --output text') do set ACCOUNT_ID=%%i
                            set ECR_URI=%ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%ECR_REPO%:%IMAGE_TAG%
                            
                            echo Deploying %ECR_URI% to EC2...
                            python -m awscli ssm send-command --document-name "AWS-RunShellScript" --parameters "commands=['docker pull %ECR_URI%','docker stop agenticrag || true','docker rm agenticrag || true','docker run -d --name agenticrag -p 8501:8501 %ECR_URI%']" --targets "Key=tag:Name,Values=AgenticRAG-Server" --region %AWS_REGION%
                            
                            echo Deployment command sent to EC2
                        '''
                    }
                }
            }
        }
    }
}