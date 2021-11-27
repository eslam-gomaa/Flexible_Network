pipeline {
//   environment { 
//     registry = "https://registry.hub.docker.com/eslamgomaa" 
//     registryCredential = 'docker_hub_id' 
//     dockerImage = '' 
//   }
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
    stage('Build the Library & Run Unit tests') {
      steps {
        container('python') {
          script {
            echo 'Building the library'
            sh 'ls -lh'
            sh  '''python3.6 setup.py bdist_wheel &&
                   pip3.6 install dist/FlexibleNetwork-*.whl'''
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
            sh "twine upload -u Eslam-Gomaa -p '0b@pGI#FbKigVBPYuYnT!oQiG5lf0a1CW'  dist/* --verbose"
          }
        }
      }
    }
  }