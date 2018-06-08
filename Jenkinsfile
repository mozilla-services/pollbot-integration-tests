pipeline {
  agent {
    dockerfile true
  }
  libraries {
    lib('fxtest@1.10')
  }
  environment {
    PROJECT = "${PROJECT ?: JOB_NAME.split('\\.')[0]}"
    TEST_ENV = "${TEST_ENV ?: JOB_NAME.split('\\.')[1]}"
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
    stage('Test pollbot') {
      steps {
        sh "pytest --env=${TEST_ENV}"
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
