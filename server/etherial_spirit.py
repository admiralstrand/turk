# -*- coding: utf-8 -*-
"""Super minimal app for the turk."""
from flask import Flask
# from flask import render_template
from flask_socketio import SocketIO
import sys
sys.path.insert(0, '/var/www/html/turk')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app)
