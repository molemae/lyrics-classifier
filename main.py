import sys
import os 
import time
from argparse import ArgumentParser
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# source download functions from other scripts
from web_sel import search_on_chrome, get_artist_url, store_link_in_list
from get_links_soup import get_lyrics_links
from scraping_soup import song_downloader
from song_bow import train_fit_pred


# It parses the command line
parser = ArgumentParser(description="This Programm will download lyrics, predict the artist of Lyrics given.")
parser.add_argument(
    "artist1",
    help="Write an artist you want to download and predict lyrics from"
)

parser.add_argument(
    "artist2",
    default=[False],
    help="write a second artist to compare train the model",
    nargs='*'
)
# parser.add_argument(
#     "link1",
#     default=[False],
#     help="link to lyrics",
#     nargs='*'
# )


# It maps the user  inputs to the arguments
#print(parser.parse_args())
user_inputs = parser.parse_args()
print(user_inputs)


# Here we extracts the user inputs
artist1 = (user_inputs.artist1)
if not user_inputs.artist2[0]:
    artist2 = 'Bob Dylan'
else:
   artist2 = user_inputs.artist2[0]

# artist_list = ('Bob Marley','Red Fang')
# retrieve links to artist webpage: 
# artist_link_zip = store_link_in_list('http://www.lyrics.com',artist1,artist2)
artist_list = (artist1, artist2)


for artist in  artist_list: #artist_link_zip:
    if artist == 'Bob Dylan':
        continue

    url = get_artist_url(artist_name=artist,url='http://www.lyrics.com')
    #  get song url list?
    get_song_urls = input(f'Get Lyrics URLs of {artist}? [y/n]')
    if get_song_urls.lower() in ['yes','y']:
        song_url_list = get_lyrics_links(artist, url)
        print(f'Found {len(song_url_list)} Songs of {artist}')
    
    
    # Download Songs
    download_lyrics = input(f'Download Lyrics from {artist}? [y/n]')
    if download_lyrics.lower() in ['yes','y']:
        no_of_songs = input(f'How many songs of {artist} would you like to download? default: all {len(song_url_list)} songs [all, [int]]')
        # if type (no_of_songs) == str:
        try:
            no_of_songs = int(no_of_songs)
        except:
            if no_of_songs.lower() == 'all':
                no_of_songs = len(song_url_list)
            else:
                no_of_songs = len(song_url_list)
                
        song_downloader(artist,no_of_songs)


print("Here's the model fit:")
if artist2 == 'Bob Dylan':
    print('[Only one artist given, using Bob Dylan as second artist in model]')
# train model
train_fit_pred(artist1,artist2)
