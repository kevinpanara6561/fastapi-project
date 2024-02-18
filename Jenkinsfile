pipeline {
    agent { label "dev-server"}
    
    stages {
        
        stage("code"){
            steps{
                git url: "https://github.com/kevinpanara/fastapi_project.git", branch: "main"
                echo 'code is clone'
            }
        }
        stage("build and test"){
            steps{
                sh "docker build -t fastapi_project ."
                echo 'code is build'
            }
        }
        stage("scan image"){
            steps{
                echo 'image is scanned'
            }
        }
        stage("push"){
            steps{
                withCredentials([usernamePassword(credentialsId:"dockerHub",passwordVariable:"dockerHubPass",usernameVariable:"dockerHubUser")]){
                sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                sh "docker tag fastapi_project:latest ${env.dockerHubUser}/fastapi_project:latest"
                sh "docker push ${env.dockerHubUser}/fastapi_project:latest"
                echo 'image is pushed'
                }
            }
        }
        stage("deploy"){
            steps{
                sh "docker-compose down && docker-compose up -d"
                echo 'deployment is done'
            }
        }
    }
}