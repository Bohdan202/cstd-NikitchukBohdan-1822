from flask import request, make_response, Blueprint, send_from_directory

app = Blueprint('admin_routes', __name__)

import time

from other.firebase import firebase

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

# @app.route("/admin", methods=['GET'])
# def admin():
#     if handler(request):
#         return send_from_directory(app.static_folder, "admin.html")
#     else:
#         return { 'status': 'bad_token' }

@app.route('/get_all_users', methods=['POST'])
def get_all_users():
    if handler(request):
        uid = request.cookies.get('uid')

        result = []
        users = firebase.get_all_users()

        for id, user in users.items():
            if (users[uid]['admin'] and users[uid]['admin'] == 'root') or (user['admin'] and user['admin'] != 'root'):
                user['id'] = id
                result.append(user)

        response = make_response({ 'status': 'ok', 'users': result })

        return response
    else:
        return { 'status': 'bad_token' }