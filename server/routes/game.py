from flask import request, make_response, Blueprint
from math import sqrt

from flask_socketio import emit

app = Blueprint('game_routes', __name__)

import time

from other.firebase import firebase
# from game.classes import Character

chars = {}
speed = 4

def handler(request):
    uid = request.cookies.get('uid')
    token = request.cookies.get('token')
    valid = False

    if (uid is not None) and (valid is not None):
        valid = firebase.get_valid(uid, token)

    # print("handler:", valid)
    return valid


@app.route('/new_player', methods=['POST'])
def new_player():
    if handler(request):
        print('new player')
        response = make_response({ 'status': 'ok' })

        uid = request.cookies.get('uid')
        user = firebase.get_user(uid)

        # chars[uid] = Character.Character(uid, user.nickname, user.photo, user.game.pos.x, user.game.pos.y)
        
        if uid not in chars:
            chars[uid] = {
                'nickname': user['nickname'],
                'img': user['photo'],
                'x': user['x'],
                'y': user['y']
            }
        else:
            chars[uid]['name'] = user['nickname']

        emit('update_user', { 'id': uid, 'user': chars[uid] }, broadcast=True, namespace='')

        return response
    else:
        return { 'status': 'bad_token' }


@app.route("/set_position", methods=['POST'])
def set_position():
    if handler(request):
        uid = request.cookies.get('uid')

        x = request.json['x']
        y = request.json['y']

        if x!=0:
            x = x/abs(x)
        if y!=0:
            y = y/abs(y)

        sp = speed
        if x!=0 and y!=0:
            sp = speed * sqrt(2)
        
        if uid in chars and 'x' in chars[uid] and 'y' in chars[uid]:
            chars[uid]['x'] += int(x) * sp
            chars[uid]['y'] += int(y) * sp

        emit('update_user', { 'id': uid, 'user': chars[uid] }, broadcast=True, namespace='')

        return { 'status': 'ok' }
    else:
        return { 'status': 'bad_token' }