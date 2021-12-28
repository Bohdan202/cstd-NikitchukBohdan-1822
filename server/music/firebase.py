from pyrebase import pyrebase
from threading import Timer
from datetime import datetime


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class FirebaseDiscrod:
    def __init__(self):  # кредли на базу данних firebase
        self.config = {
            "apiKey": "AIzaSyAM8uhj4EDvrpcwo5gp3KfRMA585JDuPyA",
            "authDomain": "diploma-db.firebaseapp.com",
            "databaseURL": "https://diploma-db-default-rtdb.europe-west1.firebasedatabase.app",
            "projectId": "diploma-db",
            "storageBucket": "diploma-db.appspot.com",
            "messagingSenderId": "794633341152",
            "appId": "1:794633341152:web:c0eabd764ddee65d8de885",
            "measurementId": "G-DKNKNT9Z53"
        }

        # початок сесії бази данних при ініціалізації програми
        self.firebase = pyrebase.initialize_app(self.config)
        # перевірка кредлів юзера при спробі аутентифікації
        self.auth = self.firebase.auth()
        self.user = self.auth.sign_in_with_email_and_password(  # кредли суперюзера для входу в програму
            "bot@mail.com", "botpassword")
        print(str(datetime.now()) + ': authentication')
        # print('id token:', self.user['idToken'])

        self.db = self.firebase.database()  # доступ до самої БД

        # ініціалізація запису токена при аутентифікації юзера
        timer = RepeatTimer(25*60, self.refresh_token)
        timer.start()

    def get_playlist(self, id):  # отримання всіх пісень введеного плейлисту з папки playlist
        return self.db.child('playlist').child(id).get(self.user['idToken']).val()

    def set_playlist(self, id, songs):  # збереження введеного плейлисту в базу данних
        self.db.child("playlist").child(id).set(songs, self.user['idToken'])
        return 'ok'

    def add_song(self, id, song):  # збереження всіх пісень поточного плейлисту в базу данних
        length = len(self.db.child("playlist").child(
            id).get(self.user['idToken']).val())
        self.db.child("playlist").child(id).update(
            {length: song}, self.user['idToken'])
        return 'ok'

    def get_all_last_playlists(self):  # отримати останній збережений плейлист
        return self.db.child('last_playlist').get(self.user['idToken']).val()

    def set_last_playlist(self, id, songs):  # зберегти останній збережений плейлист
        self.db.child("last_playlist").child(
            id).set(songs, self.user['idToken'])
        return 'ok'

    def remove_last_playlist(self, id):  # видалити останній збережений плейлист
        self.db.child("last_playlist").child(id).remove(self.user['idToken'])
        return 'ok'

    def refresh_token(self):  # змінити кредли поточного юзера
        self.user = self.auth.refresh(self.user['refreshToken'])
        print(str(datetime.now()) + ': refresh')

    def report(self, message):  # сповістити про помилку при спробі аутентифікації поточного юзера
        time = str(datetime.now()).replace('.', '_')
        self.db.child("report").update({time: message})


firebase = FirebaseDiscrod()
