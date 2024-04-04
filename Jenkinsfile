pipeline {
    agent any 
    
    stages {
        stage("Clone Code") {
            steps {
                echo "Cloning the code"
                git url: "https://github.com/kevinpanara/fastapi_project.git", branch: "main"
                echo "Cloned the code"
            }
        }
        stage("Build") {
            steps {
                echo "Building the image"
                sh "docker build -t fastapi_project ."
                echo "Built the image"
            }
        }
        stage("Deploy to Remote EC2") {
            agent {
                // Set up the SSH agent to connect to the remote EC2 instance
                sshagent (credentials: ['ubuntu']) {
                    // Provide the remote EC2 instance details
                    node {
                        // Execute commands on the remote EC2 instance
                        echo "Deploying the container to remote EC2"
                        sh "scp -i .ssh/id_rsa docker-compose.yml user@remote_host:/home/ubuntu"
                        sh "scp -i .ssh/id_rsa Dockerfile user@remote_host:/home/ubuntu"
                        sh "docker save fastapi_project | gzip | ssh -i .ssh/id_rsa user@remote_host 'gunzip | docker load'"
                        sshScript remote: 'user@remote_host', script: 'docker-compose down && docker-compose up -d'
                        echo "Deployed the container to remote EC2"
                    }
                }
            }
        }
    }
}
