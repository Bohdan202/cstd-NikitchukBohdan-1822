
# from flask import request
# from flask_socketio import SocketIO, send, emit
# from server import socketio

# import time
# # import os

# @socketio.on('connect')
# def connect():
#     uid = request.cookies.get('uid')
#     print('Client connected:', uid)

# @socketio.on('disconnect')
# def chat_disconnect():
#     uid = request.cookies.get('uid')
#     print ("Client disconnected:", uid)


# # def send_all_users():
# #     print(123)
# #     socketio.emit('all_users', chars, broadcast=True, namespace='')

# # from threading import Timer
# # class RepeatTimer1(Timer):
# #     def run(self):
# #         while not self.finished.wait(self.interval):
# #             self.function(*self.args, **self.kwargs)

# # timer2 = RepeatTimer1(1, send_all_users)
# # timer2.start()


# @socketio.on('message')
# def handleMessage(msg):
# 	print('Message: ' + msg)
# 	send(msg, broadcast=True)