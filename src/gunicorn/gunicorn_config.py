import os
import multiprocessing


def num_cpus():
    cpus = 0
    try:
        cpus = os.sysconf('SC_NPROCESSORS_ONLN')
    except:
        cpus = multiprocessing.cpu_count()
    return cpus or 3


name = 'web-notify'
bind = '0.0.0.0:5000'
# workers = num_cpus() * 2 + 1
workers = 1
debug = True
daemon = False
loglevel = 'debug'
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
