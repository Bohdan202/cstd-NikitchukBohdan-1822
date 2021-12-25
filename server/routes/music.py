from flask import request, make_response, Blueprint

app = Blueprint('music_routes', __name__)

from music.spotify import get_splaylist
from music.youtube_downloader import search

# import time

from other.firebase import firebase

@app.route('/get_playlist', methods=['GET', 'POST'])
def get_playlist():
    # handler(request)
    playlist = request.json['playlist']
    result = firebase.get_playlist(playlist)
    return { 'songs': result }

@app.route('/set_playlist', methods=['POST'])
def set_playlist():
    playlist = request.json['playlist']
    songs = request.json['songs']

    temp = {}

    for i, song in enumerate(songs):
        temp[i] = song

    firebase.set_playlist(playlist, temp)

    return { 'status': 'OK' }

@app.route('/get_spotify', methods=['GET', 'POST'])
def get_spotify():
    # handler(request)
    link = request.json['link']
    result = get_splaylist(link)
    return { 'songs': result }

# @app.route('/play', methods=['GET', 'POST'])
# def play():
#     id = request.json['id']
#     # songs = request.json['songs']
#     songs = ['chromance wrap me in plastic', 'marwa loud bad boy' 'nicki minaj starships', 'one direction what makes you beautiful', 'mother mother hay loft', 'almyr jules take a little time', 'dirty heads vacation']
#     number = request.json['number']
#     discordbot.stop(id)
#     discordbot.play(id, songs, number)

@app.route('/get_source', methods=['POST'])
def get_source():
    try:
        name = request.json['name']
        _, source = search(name + ' audio')

        return { 'source': source }
    except:
        return { 'source': '' }