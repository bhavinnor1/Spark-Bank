pipeline {
    agent any
    stages {
    stage('git clone') {
            steps {
              git branch: 'main', url: 'https://github.com/hbtufiftyone/Spark-Bank'
            }
    }
         stage(' push image to hub'){
            steps{
                script{
                    withCredentials([string(credentialsId: 'dockerhub', variable: 'passwd')]) {
                      sh 'docker login -u sachin887 -p ${passwd}'
                        sh 'docker build -t sachin887/assignment .'
                    }
                   
                      sh "docker push sachin887/assignment:latest"
                }
            }
        }
        stage('deploy to k8s') {
            steps{
                scripts {
                    withCredentials([file(credentialsId: 'deployee', variable: 'test')]) {
                       sh "kubectl create -f deployment.yml ."
                         sh "kubectl create -f Servicefile.yml ."
                    }
                }
            }
        }
  
         
    }
}
