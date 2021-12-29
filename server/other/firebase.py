from pyrebase import pyrebase
from threading import Timer
from datetime import datetime


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class FirebaseServer:
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

        
        self.firebase = pyrebase.initialize_app(self.config) # початок сесії бази данних при ініціалізації програми

        
        self.auth = self.firebase.auth() # перевірка кредлів юзера при спробі аутентифікації
        self.storage = self.firebase.storage()  # доступ до данних БД

        self.user = self.auth.sign_in_with_email_and_password(
            "server@mail.com", "server@pas$word72")  # кредли суперюзера для входу в програму

        # звірка поточної дати при аутентифікації юзера
        print(str(datetime.now()) + ': authentication')
        # print('id token:', self.user['idToken'])

        self.db = self.firebase.database()  # доступ до самої БД

        
        timer = RepeatTimer(25*60, self.refresh_token) # ініціалізація запису токена при аутентифікації юзера
        timer.start()

    def get_playlist(self, id): # отримання всіх пісень введеного плейлисту з папки playlist
        return self.db.child('playlist').child(id).get(self.user['idToken']).val()

    def set_playlist(self, id, songs): # збереження введеного плейлисту в базу данних
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

    # редагувати данні юзера в адмін панелі
    def update_user(self, uid, token, nickname, email, photo, pos=None):
        user = {
            'nickname': nickname,
            'email': email,
            'photo': photo
        }
        if pos:
            user['game'] = {'pos': {}}
            user['game']['pos']['x'] = pos['x']
            user['game']['pos']['y'] = pos['y']

        print("uid2:", uid)
        self.db.child("users").child(uid).update(user, token)

    def get_user(self, uid, token=None):  # вивести всі данні про юзера в адмін панель
        if not token:
            nickname = self.db.child("users").child(uid).child(
                'nickname').get(self.user['idToken']).val()
            photo = self.db.child("users").child(uid).child(
                'photo').get(self.user['idToken']).val()

            x = self.db.child("users").child(uid).child('game').child(
                'pos').child('x').get(self.user['idToken']).val()
            y = self.db.child("users").child(uid).child('game').child(
                'pos').child('y').get(self.user['idToken']).val()

            user = {
                'nickname': nickname,
                'photo': photo,
                'x': x or 0,
                'y': y or 0
            }

            return user

        else:
            nickname = self.db.child("users").child(
                uid).child('nickname').get(token).val()
            photo = self.db.child("users").child(
                uid).child('photo').get(token).val()

            user = {
                'nickname': nickname,
                'photo': photo
            }

            return user

    def refresh_token(self, refresh=None):  # змінити кредли поточного юзера
        if refresh:
            user = self.auth.refresh(refresh)
            # print(user)
            return user['idToken']
        else:
            self.user = self.auth.refresh(self.user['refreshToken'])
            print(str(datetime.now()) + ': refresh')

    def report(self, message):  # сповістити про помилку при спробі аутентифікації поточного юзера
        time = str(datetime.now()).replace('.', '_')
        self.db.child("report").update({time: message})

    def test(self, message):  # отримати час реєстрації юзера
        time = str(datetime.now()).replace('.', '_')
        self.db.child("test").update({time: message})

    # створити початок сесії використання програми поточного юзера
    def make_session(self, uid, token):
        # time = str(datetime.now()).replace('.', '_')
        self.db.child("session").update({uid: token}, self.user['idToken'])

    def get_valid(self, uid, token):  # перевірка валідності данних юзера
        # time = str(datetime.now()).replace('.', '_')
        from_db = self.db.child("session").child(
            uid).get(self.user['idToken']).val()
        return from_db == token

    # перевірка валідності данних адміна на доступ до відповідних фінкцій його ролі
    def get_admin(self, uid):
        # time = str(datetime.now()).replace('.', '_')
        from_db = self.db.child("users").child(uid).child(
            'admin').get(self.user['idToken']).val()
        return from_db

    def get_all_users(self):  # отримати всіх юзерів не залежно від їх ролі
        from_db = self.db.child("users").get(self.user['idToken']).val()
        return from_db

    def get_img(self):  # отримати фото поточного юзера
        result = self.storage.child("images").child(
            "53675bb67a77.jpg").get_url(self.user['idToken'])
        # files = self.storage.child("images").list_files()
        # for file in files:
        #     print(self.storage.child(file.name).get_url(None))
        # print(12345, result)
        return result
        # return 'ok'


firebase = FirebaseServer()
