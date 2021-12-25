from flask import request, redirect, render_template, send_from_directory, url_for, make_response
from flask import Flask
from flask.globals import current_app
from flask_cors import CORS

from routes.music import app as music_routes
from routes.auth import app as auth_routes
from routes.game import app as game_routes, chars
from routes.storage import app as storage_routes
from routes.admin import app as admin_routes

from flask_socketio import SocketIO, send, emit
import pusher

# import asyncio

import time
import os

from config import token, app_id, public_key

from other.firebase import firebase

app = Flask(__name__, static_url_path='', static_folder='static')
# app.config['SERVER_NAME'] = 'app-72.herokuapp.com'

app.register_blueprint(music_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(game_routes)
app.register_blueprint(storage_routes)
app.register_blueprint(admin_routes)

ORIGINS = [
    'http://localhost:8080',
    'http://localhost:5000',
    'http://127.0.0.1:8080',
    'https://app72-63cf0.web.app/',
    'https://app-72.herokuapp.com/'
]

CORS(app, resources={ r'/*': {'origins': ORIGINS}}, supports_credentials=True)

# socketio = SocketIO(app, cors_allowed_origins="*", message_queue='redis://', async_mode=None)
socketio = SocketIO(app, cors_allowed_origins="*")

pusher_client = pusher.Pusher(
  app_id='1257972',
  key='11a3c34b3c5456540148',
  secret='4272e6c4ce94ff9cd8b9',
  cluster='eu',
  ssl=True
)

def handler(request):
    uid = request.cookies.get('uid')
    token = request.cookies.get('token')
    valid = False

    if (uid is not None):
        valid1 = firebase.get_valid(uid, token)
        valid2 = firebase.get_admin(uid)
        
        valid = valid1 and valid2

    # print("handler:", valid)
    return valid

@app.route("/admin", methods=['GET'])
def admin():
    if handler(request):
        return send_from_directory(app.static_folder, "admin.html")
    else:
        return { 'status': 'bad_token' }

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/", subdomain="music", methods=['GET'])
def music():
    return send_from_directory(app.static_folder, "music.html")

@app.route("/m", methods=['GET'])
def music1():
    return send_from_directory(app.static_folder, "music.html")

@app.route('/check', methods=['GET', 'POST'])
def check():
    return "OK"

@app.route('/test_sleep5', methods=['GET', 'POST'])
def test_sleep():
    time.sleep(5)
    return { 'value': 'Hello' }

@app.route('/test_pusher', methods=['GET', 'POST'])
def test_pusher():
    pusher_client.trigger('mychannel', 'myevent', {'message': 'hello world'})
    return { 'status': 'OK' }

# @socketio.on('connect')
# def connect():
#     uid = request.cookies.get('uid')
#     print('Client connected:', uid)

# @socketio.on('disconnect')
# def chat_disconnect():
#     uid = request.cookies.get('uid')
#     print ("Client disconnected:", uid)


current_time = {}
current_chat_time = {}
last_messages = []
count_last_messages = 20

from math import sqrt
from datetime import datetime

@socketio.on("set_position")
def set_position(arg=None):
    speed = 4

    uid = request.cookies.get('uid')

    if uid in current_time:
        if (time.time()-current_time[uid]>0.05):

            # print('time:', time.time())
                
            x = arg['x']
            y = arg['y']

            if x!=0:
                x = x/abs(x)
            if y!=0:
                y = y/abs(y)

            sp = speed
            if x!=0 and y!=0:
                sp = speed / sqrt(2)
            
            if uid in chars and 'x' in chars[uid] and 'y' in chars[uid]:
                chars[uid]['x'] += int(x) * sp
                chars[uid]['y'] += int(y) * sp

            emit('update_user', { 'id': uid, 'user': chars[uid] }, broadcast=True, namespace='')

            current_time[uid] = time.time()
    else:
        current_time[uid] = time.time()

# @socketio.on("send_message")
# def send_message(arg=None):
#     print("send message")
#     uid = request.cookies.get('uid')

#     if uid:
#         if not uid in current_chat_time or time.time()-current_chat_time[uid]>0.1:
#             if not uid in current_chat_time:
#                 current_chat_time[uid] = time.time()
            
#             user = firebase.get_user(uid)
#             c_time = datetime.now()

#             hour = str(c_time.hour) if c_time.hour>=10 else '0' + str(c_time.hour)
#             minute = str(c_time.minute) if c_time.minute>=10 else '0' + str(c_time.minute)
#             second = str(c_time.second) if c_time.second>=10 else '0' + str(c_time.second)

#             curr_time = hour + ':' + minute + ':' + second

#             message = {
#                 'id': uid,
#                 'user': {
#                     'nickname': user['nickname'],
#                     'photo': user['photo'],
#                 },
#                 'message': arg['message'],
#                 'time': curr_time
#             }
            
#             if len(last_messages)>:
#                 last_messages.pop(0)

#             last_messages.append(message)

#             emit('new_message', message, broadcast=True, namespace='')

#             current_chat_time[uid] = time.time()
#         else:
#             emit('new_message', {
#                 'id': 'server',
#                 'user': {
#                     'nickname': 'server',
#                     'photo': 'server'
#                 },
#                 'message': 'wait, not so fast',
#                 'time': ''
#                 }, namespace='')

@app.route('/send_message', methods=['GET', 'POST'])
def send_message(arg=None):
    print("send message")
    uid = request.cookies.get('uid')
    arg = request.json

    if uid:
        if not uid in current_chat_time or time.time()-current_chat_time[uid]>0.1:
            if not uid in current_chat_time:
                current_chat_time[uid] = time.time()
            
            user = firebase.get_user(uid)
            c_time = datetime.now()

            hour = str(c_time.hour) if c_time.hour>=10 else '0' + str(c_time.hour)
            minute = str(c_time.minute) if c_time.minute>=10 else '0' + str(c_time.minute)
            second = str(c_time.second) if c_time.second>=10 else '0' + str(c_time.second)

            curr_time = hour + ':' + minute + ':' + second

            message = {
                'id': uid,
                'user': {
                    'nickname': user['nickname'],
                    'photo': user['photo'],
                },
                'message': arg['message'],
                'time': curr_time
            }
            
            if len(last_messages)>count_last_messages:
                last_messages.pop(0)

            last_messages.append(message)

            pusher_client.trigger('chat', 'new_message', message)

            current_chat_time[uid] = time.time()
            return { 'status': 'OK' }
        else:
            pusher_client.trigger('chat', 'new_message', {
                'id': 'server',
                'user': {
                    'nickname': 'server',
                    'photo': 'server'
                },
                'message': 'wait, not so fast',
                'time': ''
                }, namespace='')
            return { 'status': 'OK' }
    else:
        return { 'status': 'OK' }

# @socketio.on("join_to_chat")
# def join_to_chat(arg=None):
#     print("join_to_chat")
#     emit('join_to_chat', { 'messages': last_messages }, namespace='')

@app.route('/join_to_chat', methods=['GET', 'POST'])
def join_to_chat():
    print("join_to_chat")
    pusher_client.trigger('chat', 'join_to_chat', { 'messages': last_messages })
    return { 'status': 'OK', 'messages': last_messages }
        
# @socketio.on('message')
# def handleMessage(msg):
# 	print('Message: ' + msg)
# 	send(msg, broadcast=True)


def start():
    # port = int(os.environ.get('PORT', 5555))

    # app.run(host='0.0.0.0', port=port)
    # firebase.report("server started")
    
    # socketio.run(app, host='0.0.0.0', port=port, debug=False)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    # socketio.run(app, host='0.0.0.0', debug=False)

    # from waitress import serve
    # serve(app, host="0.0.0.0", port=port, _quiet=True)


# start()

if __name__ == "__main__":
#     discthread.start()
    start()