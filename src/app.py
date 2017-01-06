#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import os
import logging
import socketio
from flask import Flask, request, render_template, jsonify

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

NAMESPACE = os.getenv('SOCKET_NAMESPACE', '/wsock')
# async_mode = None
async_mode = 'gevent'

sio = socketio.Server(logger=True, async_mode=async_mode)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'secret!')
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)


def all_clients():
    return sio.manager.rooms[NAMESPACE][None].keys()


@app.route('/')
def app_index():
    return render_template('index.html')


@app.route('/push/<room>', methods=['POST'], strict_slashes=False)
def app_push(room=None):
    if not request.is_json:
        return jsonify({
            'error': 'Must push json formated data!'
        }), 400
    content = request.get_json().copy()
    content['room'] = room
    logger.info('Push content to %s: %r', room, content)
    sio.emit('push', content, room=room, namespace=NAMESPACE)
    return jsonify({})


@sio.on('connect', namespace=NAMESPACE)
def sio_connect(sid, environ):
    logger.info('Client connected: %r (%d)', sid, len(all_clients()))


@sio.on('disconnect', namespace=NAMESPACE)
def sio_disconnect(sid):
    logger.info('Client connected: %r (%d)', sid, len(all_clients()))


@sio.on('join', namespace=NAMESPACE)
def sio_join(sid, message):
    room = message['room']
    sio.enter_room(sid, room, namespace=NAMESPACE)
    content = {
        'data': 'In room: %r' % room,
    }
    logger.info('Client %r joining room: %r', sid, room)
    sio.emit('push', content, room=sid, namespace=NAMESPACE)


@sio.on('leave', namespace=NAMESPACE)
def sio_leave(sid, message):
    room = message['room']
    sio.leave_room(sid, room, namespace=NAMESPACE)
    content = {
        'data': 'Not in room: %r' % room,
    }
    logger.info('Client %r leaving room: %r', sid, room)
    sio.emit('push', content, room=sid, namespace=NAMESPACE)


@sio.on('push', namespace=NAMESPACE)
def sio_push(sid, message):
    logger.info('Message from client %s: %r', sid, message)


if __name__ == '__main__':
    if sio.async_mode == 'gevent':
        from gevent import pywsgi
        kwargs = {}
        try:
            from geventwebsocket.handler import WebSocketHandler
            kwargs['handler_class'] = WebSocketHandler
        except ImportError:
            pass
        pywsgi.WSGIServer(('', 5000), app, **kwargs).serve_forever()
    else:
        import eventlet
        import eventlet.wsgi
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
