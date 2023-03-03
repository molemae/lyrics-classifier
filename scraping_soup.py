# Importing
import os
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def song_downloader(artist,no_of_songs=False):
    '''
    !!! looks for a {name}_names_and_links.csv file created 
        by get_links_soup.py in ./data/ !!!
    '''
        
    # open link file
    links_in = pd.read_csv(f'data/{artist}_names_and_links.csv', sep=";")
    links_in = links_in.reset_index()
    # define header to avoid getting blacklisted
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


    # check if path to 
    path =  f'./data/{artist}'
    if not os.path.exists(path):
        os.makedirs(path)


    try: songs_downloaded
    except:
        songs_downloaded = list()
    try: empty_links
    except:
        empty_links = list()
    # testsonglist = list()
    for idx, row in links_in.iterrows():
        print(idx)
        if idx == no_of_songs+1:
            break
        # if idx == 100:
        #     break
        # check iteration 
        if not idx%10:
            print(f'iteration: {idx}')

        #rename names and links for readability
        name = row[1]
        link = row[2]

        # check if song is already downloaded:
        name = name.split('[',)[0].rstrip().lower()
        if name in songs_downloaded:
            print('Song already downloaded,skipping')
            continue
        # check if link was already checked and found empty:
        if link in empty_links:
            print('Empty Link: previously checked')
            continue


        # Scraping

        time.sleep(3)

        # get website
        response = requests.get(url=link)
        song_html = response.text
        soup = BeautifulSoup(markup=song_html, features='html.parser')

        try:
            songtext = soup.find(name='pre').get_text()
        except:
            print(f'No text found: {name}')
            empty_links.append(link)
            continue
        # Download successfull, append to downloaded list:
        songs_downloaded.append(name)
        
        file_name = name.replace(' ','_').replace('/','_')

        # save to file
        with open(file= f'{path}/{file_name}.txt', mode='w') as file:
            file.write(songtext) 

    print(f'Done \n Songs Donwloaded:{len(songs_downloaded)}')
    # save empty links to 

# artist = 'tallest_man_on_earth'

# song_downloader(artist=artist)
