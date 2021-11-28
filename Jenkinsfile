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
            slackSend color: 'good', message: "FlexibleNetwork library built successfully & Uploaded to PyPi \n Build number: ${env.BUILD_NUMBER}"
          }
        }
      }
    }
  }