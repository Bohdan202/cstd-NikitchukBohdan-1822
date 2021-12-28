# from pytube import YouTube
# from pytube import Playlist
from youtube_dl import YoutubeDL
from requests import get
import os

#get videos from links or from youtube search
def search(arg, download=False):
    try:
        with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
            try: get(arg)
            except: info = ydl.extract_info(f"ytsearch:{arg}", download=download)['entries'][0]
            else: info = ydl.extract_info(arg, download=download)
        return (info, info['formats'][0]['url'])
    except:
        print('\n\nERROR ', arg, '\n\n')

        with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
            try: get(arg)
            except: info = ydl.extract_info(f"ytsearch:{arg}", download=download)['entries'][0]
            else: info = ydl.extract_info(arg, download=download)
        return (info, info['formats'][0]['url'])


# def download_music(url, path=None):
#     YouTube(url).streams.filter(only_audio=True).first().download(path)

def get_music(arg):
    info, _ = search(arg, True)
    
    v_id = info['id']
    title = info['title']
    ext = info['ext']

    file_name = title + '-' + v_id + '.' + ext

    return title, file_name


# get_music('shape of you')