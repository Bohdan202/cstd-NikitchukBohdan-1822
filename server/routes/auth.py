from flask import request, make_response, Blueprint

app = Blueprint('auth_routes', __name__)

import time

from other.firebase import firebase

# @app.route('/getcookie', methods=['GET', 'POST'])
# def getcookie():
#     print(1)
#     cookies = request.cookies
#     print(2, cookies)
#     t = request.cookies.get('uid')
#     print(3, t)
#     return { 'cookies': cookies }

# @app.route('/send_authdata', methods=['POST'])
# def send_authdata():
#     uid = request.json['uid']
#     googletoken = request.json['googletoken']
    
#     firebase.test(uid)
#     firebase.test(googletoken)

#     return { 'status': 'ok' }

@app.route('/new_user', methods=['POST'])
def new_user():
    uid = request.cookies.get('uid')
    token = request.cookies.get('token')

    name = request.json['name']
    email = request.json['email']
    photo = request.json['photo']

    # print('new user:', name, email, photo)
    
    firebase.update_user(uid, token, name, email, photo, pos={'x': 0, 'y': 0})

    return { 'status': 'ok' }

# @app.route('/get_user_data', methods=['POST'])
# def get_user_data():
#     setCookie, token = handler(request)
#     uid = request.cookies.get('uid')
    
#     user = firebase.get_user(uid, token)

#     response = make_response({ 'status': 'ok', 'user': user })
#     setCookie(response)

#     if not token:
#         return { 'status': 'bad_token' }

#     return response

# @app.route('/refresh_token', methods=['POST'])
# def refresh_token():
#     refresh = request.cookies.get('refresh')
#     token = firebase.refresh_token(refresh)

#     resp = make_response()
#     resp.set_cookie('token', token)
#     resp.set_cookie('expiration', str(time.time() + 60*60))

#     return resp, token

# def handler(request):
#     expiration = request.cookies.get('expiration')
#     refresh = request.cookies.get('refresh')
#     if (expiration and refresh):
#         if (time.time()*1000 > float(expiration)):
#             token = firebase.refresh_token(refresh)

#             def setCookie(response):
#                 response.set_cookie('token', token)
#                 response.set_cookie('expiration', str(time.time() + 60*60))

#             return setCookie, token
#         else:
#             token = request.cookies.get('token')
#             return lambda response: _, token
#     else:
#         return lambda response: _, None

def handler(request):
    uid = request.cookies.get('uid')
    token = request.cookies.get('token')
    valid = False

    if (uid is not None) and (valid is not None):
        valid = firebase.get_valid(uid, token)

    # print("handler:", valid)
    return valid

@app.route('/make_session', methods=['POST'])
def make_session():
    uid = request.cookies.get('uid')
    token = request.cookies.get('token')
    
    firebase.make_session(uid, token)

    response = make_response({ 'status': 'ok' })

    if not token:
        return { 'status': 'bad_token' }

    return response

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    if handler(request):
        uid = request.cookies.get('uid')
        
        user = firebase.get_user(uid)
        response = make_response({ 'status': 'ok', 'user': user })

        return response
    else:
        return { 'status': 'bad_token' }