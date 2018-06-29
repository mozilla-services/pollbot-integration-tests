pipeline {
  agent {
    dockerfile true
  }
  libraries {
    lib('fxtest@1.10')
  }
  environment {
    PROJECT = "${PROJECT ?: JOB_NAME.find('\\.') ? JOB_NAME.split('\\.')[0] : ''}"
    TEST_ENV = "${TEST_ENV ?: JOB_NAME.find('\\.') ? JOB_NAME.split('\\.')[1] : ''}"
  }
  triggers {
    pollSCM('H/5 * * * *')
    cron('H H * * *')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  stages {
    stage('Lint') {
      steps {
        sh "flake8"
      }
    }
    stage('Test') {
      parallel {
        stage('pollbot.stage') {
          when {
            anyOf {
              not { environment name: 'CHANGE_ID', value: '' }
              allOf {
                environment name: 'PROJECT', value: 'pollbot';
                environment name: 'TEST_ENV', value: 'stage'
              }
            }
          }
          steps {
            sh "pytest --env=stage"
          }
        }
        stage('pollbot.prod') {
          when {
            anyOf {
              not { environment name: 'CHANGE_ID', value: '' }
              allOf {
                environment name: 'PROJECT', value: 'pollbot';
                environment name: 'TEST_ENV', value: 'prod'
              }
            }
          }
          steps {
            sh "pytest --env=prod"
          }
        }
      }
    }
  }
  post {
    failure {
      ircNotification('#storage')
      ircNotification('#fx-test-alerts')
      emailext(
        attachLog: true,
        body: '$BUILD_URL\n\n$FAILED_TESTS',
        replyTo: '$DEFAULT_REPLYTO',
        subject: '$DEFAULT_SUBJECT',
        to: '$DEFAULT_RECIPIENTS')
    }
  }
}
