# web-notify
This is small server app that provides server push notifications to the web client using WebSocket with fallback to other transport mechanism.


## RUN
~~~~~
# if you using docker just `make`
source gunicorn/env.sh; gunicorn --config=gunicorn/gunicorn_config.py app:app
# add client to some room i.e. 450
# push from your server
curl -v -H "Content-Type: application/json" -X POST -d '{"data":"Wellcome to web-notify"}' http://localhost:5000/push/450
~~~~~
