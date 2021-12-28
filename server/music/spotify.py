import requests
from bs4 import BeautifulSoup as BS

def get_splaylist(link):
    
    response = requests.get(link)
    response = BS(response.content, 'html.parser')
    response = response.select(".tracklist-col")
    
    result = []

    for element in response:
        try:
            song = element.select_one('.track-name').text
            singer = element.select_one('.artists-albums').select_one('span').text

            result.append(song + ' ' + singer)

        except:
            pass
    
    return result