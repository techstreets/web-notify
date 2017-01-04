# web-notify
This is small server app that provides server push notifications to the web client using WebSocket with fallback to other transport mechanism.


## RUN
cd src
gunicorn --config=.././gunicorn/gunicorn_config.py app:app
