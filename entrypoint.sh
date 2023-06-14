#!/usr/bin/env sh
# 后台启动Celery
nohup celery -A wsgi_gunicorn:celery_app worker -f ./logs/celery.log -l INFO &
# 启动FlaskAPP
gunicorn -c config/gun.conf wsgi_gunicorn:app
