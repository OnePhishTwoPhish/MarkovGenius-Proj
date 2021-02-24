import configparser
import requests
from bs4 import BeautifulSoup

def getAccessToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']

token = getAccessToken()
print(token)

def searchMusicArtist(name):
    api_url = "https://api.genius.com/search?q={}".format(name)
    headers = {"authorization": token}
    r = requests.get(api_url, headers=headers)
    return r.json()

def getArtistID(name):
    r = searchMusicArtist(name)
    id = r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id

def getTopTenSongs(name):
    id = getArtistID(name)
    api_url = "https://api.genius.com/artists/{}/songs".format(id) 
    headers = {"authorization": token}
    params = {
        "sort": "popularity",
        "per_page": 10

    }
    r = requests.get(api_url, headers=headers)
    return r.json()

def getLyricsArray(name):
    r = getTopTenSongs(name)
    songs = r["response"]["songs"]
    url_objs = []
    for song in songs:
        url_objs.append(song["url"])
    return url_objs



def scrapeLyricText(name):
    links = getLyricsArray("name")
    song_lyrics = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div = soup.find(class_="lyrics")
        anchor_tags = lyrics_div.find_all('a')
        current_lyrics=[]
        for anchor in anchor_tags:
            if (len(anchor.text)>0 and anchor.text[0] != "["):
                text = anchor.text.replace("\n", " NEWLINE ")
                current_lyrics.append(text)
        song_lyrics.append(current_lyrics)
    return song_lyrics


