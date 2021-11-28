pipeline {
  environment {
    PYPI = credentials('pypi_id')  
  }
  agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        metadata:
          name: cd
          namespace: build
          label:
            app: python
        spec:
          serviceAccountName: staging-prod-create
          containers:
          - name: python
            image: python:3.6-buster
            command: ["sleep"]
            args: ["100000"]
            tty: true
            volumeMounts:
            - name: docker-socket
              mountPath: /var/run/docker.sock
              workingDir: /workspace
          volumes:
          - name: docker-socket
            hostPath:
              path: /var/run/docker.sock
              type: Socket
        '''
    }
  }
  post {  
        //  always {  
        //      slackSend color: 'good', message: "always"
        //  }  
         success {  
             slackSend color: 'good', message: "💚 \nJob name: ${env.JOB_NAME} \nBuild number: ${env.BUILD_NUMBER} \nBuild URL: ${env.BUILD_URL} \n`FlexibleNetwork` library *built successfully* & Uploaded to PyPi"
         }  
         failure {  
             slackSend color: 'danger', message: "💣 \nJob name: ${env.JOB_NAME} \nBuild number: ${env.BUILD_NUMBER} \nBuild URL: ${env.BUILD_URL} \n`FlexibleNetwork` library *build failed*"
            //  mail bcc: '', body: "<b>Example</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", cc: '', charset: 'UTF-8', from: '', mimeType: 'text/html', replyTo: '', subject: "ERROR CI: Project name -> ${env.JOB_NAME}", to: "foo@foomail.com";  
         }  
         unstable {  
             slackSend color: 'danger', message: "💣 \nJob name: ${env.JOB_NAME} \nBuild number: ${env.BUILD_NUMBER} \nBuild URL: ${env.BUILD_URL} \n`FlexibleNetwork` library *build failed* (Unstable)" 
         }  
        //  changed {  
        //      echo 'Changed.'
        //      echo 'This will run only if the state of the Pipeline has changed'  
        //      echo 'For example, if the Pipeline was previously failing but is now successful'  
        //  }  
     } 
  stages {
    stage('Cloning the Git Repo') { 
      steps { 
        git branch: 'master',
            credentialsId: 'github_id',
            url: 'https://github.com/eslam-gomaa/Flexible_Network.git'
        sh 'pwd'
        sh 'ls -lh'
      }
    }
    stage('Build the Library') {
      steps {
        container('python') {
          script {
            echo 'Building the library'
            sh 'ls -lh'
            sh  '''python3.6 setup.py bdist_wheel &&
                   pip3.6 install dist/FlexibleNetwork-*.whl'''
          }
        }
      }
    }
    stage('Run Unit tests') {
      steps {
        container('python') {
          script {
            echo 'Run Unit tests'
            // Need to be written 😅
          }
        }
      }
    }
    stage('Run Integration tests') {
      steps {
        container('python') {
          sh 'ls -lh'
        //   Will be written soon.
        }
      }
    }
    stage('Push library to PyPi') {
      steps {
        container('python') {
            sh 'pip3.6 install twine'
            sh "twine upload --skip-existing -u ${PYPI_USR} -p '${PYPI_PSW}'  dist/* --verbose"
          }
        }
      }
    }
  }