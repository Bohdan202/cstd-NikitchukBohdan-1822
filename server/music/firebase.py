from pyrebase import pyrebase
from threading import Timer
from datetime import datetime


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class FirebaseDiscrod:
    def __init__(self):
        self.config = {
            'apiKey': "AIzaSyAPYIOlqxXvro99MC2gjEcO_-oF4g5vQKk",
            'authDomain': "app72-63cf0.firebaseapp.com",
            'databaseURL': "https://app72-63cf0-default-rtdb.europe-west1.firebasedatabase.app",
            'projectId': "app72-63cf0",
            'storageBucket': "app72-63cf0.appspot.com",
            'messagingSenderId': "786370777538",
            'appId': "1:786370777538:web:c96774286589f98faa065b"
        }

        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()
        self.user = self.auth.sign_in_with_email_and_password("bot@mail.com", "botpassword")
        print(str(datetime.now()) + ': authentication')
        # print('id token:', self.user['idToken'])

        self.db = self.firebase.database()

        timer = RepeatTimer(25*60, self.refresh_token)
        timer.start()

    def get_playlist(self, id):
        return self.db.child('playlist').child(id).get(self.user['idToken']).val()

    def set_playlist(self, id, songs):
        self.db.child("playlist").child(id).set(songs, self.user['idToken'])
        return 'ok'

    def add_song(self, id, song):
        length = len(self.db.child("playlist").child(id).get(self.user['idToken']).val())
        self.db.child("playlist").child(id).update({ length: song }, self.user['idToken'])
        return 'ok'

    def get_all_last_playlists(self):
        return self.db.child('last_playlist').get(self.user['idToken']).val()
    
    def set_last_playlist(self, id, songs):
        self.db.child("last_playlist").child(id).set(songs, self.user['idToken'])
        return 'ok'

    def remove_last_playlist(self, id):
        self.db.child("last_playlist").child(id).remove(self.user['idToken'])
        return 'ok'

    def refresh_token(self):
        self.user = self.auth.refresh(self.user['refreshToken'])
        print(str(datetime.now()) + ': refresh')

    def report(self, message):
        time = str(datetime.now()).replace('.', '_')
        self.db.child("report").update({ time: message })


firebase = FirebaseDiscrod()