pipeline {
  agent any
    stages {
      stage('Deploy to Astronomer') {
       when {
        expression {
          return env.GIT_BRANCH == "origin/main"
        }
       }
       steps {
         script {
               sh 'curl https://goreleaserdev.blob.core.windows.net/goreleaser-test-container/releases/1.3.0/cloud-cli_1.3.0_Linux_x86_64.tar.gz -o astrocloudcli.tar.gz'
               sh 'tar xzf astrocloudcli.tar.gz'
               sh './astrocloud deploy ${DEPLOYMENT_ID} -f'
         }
       }
     }
   }
 post {
   always {
     cleanWs()
   }
  }
}