from flask import request, make_response, Blueprint
from math import sqrt

from flask_socketio import emit

app = Blueprint('storage_routes', __name__)

import time

from other.firebase import firebase
# from game.classes import Character


def handler(request):
    uid = request.cookies.get('uid')
    token = request.cookies.get('token')
    valid = False

    if (uid is not None) and (valid is not None):
        valid = firebase.get_valid(uid, token)

    # print("handler:", valid)
    return valid


@app.route("/get_img", methods=['POST'])
def get_img():
    print(222)
    a = firebase.get_img()
    print('img', a)

    return { 'status': 'ok', 'data': a }