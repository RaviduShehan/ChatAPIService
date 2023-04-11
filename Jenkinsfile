pipeline {
    agent any
    environment {
        dockerImageName = "shehan97105/chatapiservice"
        dockerImage = null
    }
    stages {
        stage('Build') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/RaviduShehan/ChatAPIService']]])
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build dockerImageName
                }
            }
        }
        stage('Push Docker Image') {
            environment {
                registryCredential = 'dockerlogin'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Run Docker Image') {
            steps {
                script {
                    dockerImage.run("-p 5001:5001")
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    kubernetesDeploy(configs: 'chat.yml', kubeconfigId: 'kubernetesconfigpwd')
                }
            }
        }
    }
}

