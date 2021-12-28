from other.firebase import firebase

class playlist:
    def __init__(self, songs = []):
        self.number = 1
        self.songs = songs
        self.status = 'start'
        self.repeat = False
        self.message = None

        self.source = None

    # def __setattr__(self, name, value):
    #     print ('setting', name, value)
    #     self.__dict__[name] = value

    def save(self, id):
        result = {}

        for i, song in enumerate(self.songs):
            result[i] = song

        firebase.set_playlist(id, result)

    def get(self, id):
        res = firebase.get_playlist(id)
        if res:
            self.songs = res

    def save_last(self, id):
        result = {}

        for i, song in enumerate(self.songs):
            result[i] = song

        firebase.set_last_playlist(id, result)