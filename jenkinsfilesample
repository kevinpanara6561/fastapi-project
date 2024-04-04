pipeline {
    agent any 
    
    stages{
        stage("Clone Code"){
            steps {
                echo "Cloning the code"
                git url:"https://github.com/kevinpanara/fastapi_project.git", branch: "main"
                echo "Cloned the code"
            }
        }
        stage("Build"){
            steps {
                echo "Building the image"
                sh "docker build -t fastapi_project ."
                echo "Built the image"
            }
        }
        stage("Push to Docker Hub"){
            steps {
                echo "Pushing the image to docker hub"
                withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerHubPass",usernameVariable:"dockerHubUser")]){
                sh "docker tag fastapi_project ${env.dockerHubUser}/fastapi_project:latest"
                sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                sh "docker push ${env.dockerHubUser}/fastapi_project:latest"
                echo "Pushed the image to docker hub"
                }
            }
        }
        stage("Deploy"){
            steps {
                echo "Deploying the container"
                sh "docker-compose down && docker-compose up -d"
                echo "Deployed the container"
                
            }
        }
    }
}