# slack_flask
Flask app for script integration with my slack team.

## GET Endpoints
- '/'
  - Simple 'Hello World' response

## POST Endpoints
- '/stock'
  - Returns stock prices

## DEV ENV
Better instructions to come, for now just a brain dump

- Clone project
  - git clone https://github.com/heyimdan/slack_flask.git
- Install Brew
  - /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
- Install Redis
  - brew install redis
  - Start up the service: redis-server /usr/local/etc/redis.conf
- Configure Heroku / Git
  - brew install heroku/brew/heroku
  - heroku login (Talk to Dan to get creds)
  - heroku git:remote -a watchful-nocbot-staging
  - git remote rename heroku heroku-staging
  - heroku git:remote -a watchful-nocbot
  - git remote rename heroku heroku-production
- Configure and install virtualenvwrapper
  - pip install virtualenvwrapper
  - export WORKON_HOME=~/Envs >> ~/.bashrc
  - source /usr/local/bin/virtualenvwrapper.sh >> ~/.bachrc
  - souce ~/.bashrc
  - mkdir -p $WORKON_HOME
  - cd slack_flask
  - mkvirtualenv nocbot
  - workon nocbot
  - pip install requirements.txt

Very good chance I missed something or mistyped something in these instructions.
