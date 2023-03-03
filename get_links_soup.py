# Import
import requests
import os
from bs4 import BeautifulSoup 



# Define get lyrics functoin 
def get_lyrics_links(name,url):
    # get artist website:    
    response = requests.get(url=url)
    artist_html = response.text


    # Find href links:
    soup = BeautifulSoup(markup=artist_html, features='html.parser')
    artist = soup.find(name = 'h1', attrs={'class':'artist'}).get_text()

    # get list of tr elements 
    tracks = (soup
            .find_all(name = 'tr')
            )

    # get track names and list
    songs = list()
    links = list()
    links_out = str()
    names_and_links_out = str('name;link\n')
    for track in tracks:
        tr = track.find(name = 'a', href=True)
        if tr is None:
            continue
        song_name = tr.get_text()
        song_name = song_name.replace(';',',')
        if song_name not in songs:
            songs.append(song_name)
            song_link = f"https://www.lyrics.com{tr['href']}"
            # print(tr['href'])
            links.append(song_link)
            links_out += f'{song_link}\n'
            names_and_links_out += f'{song_name};{song_link}\n'
            # --> Append both song name and link to text in csv style, in order to read them in later


    if not os.path.exists('./data/'):
        os.makedirs('./data/')
    # save only links to file
    with open(file=f'./data/{name}_links.txt', mode='w') as file:
        file.write(links_out)
    
    # save name and links to csv-file
    with open(file=f'./data/{name}_names_and_links.csv', mode='w',) as file:
        file.write(names_and_links_out)
    
    return links


# # Bob Dylan
# name = 'bob_dylan'
# URL = 'https://www.lyrics.com/artist/Bob-Dylan/4147'


# art_dict = {
#     'bob_dylan':'https://www.lyrics.com/artist/Bob-Dylan/4147',
#     'tallest_man_on_earth':'https://www.lyrics.com/artist/The-Tallest-Man-on-Earth/865422'

# }
# #bob_list = get_lyrics_links(name, URL)

# name = 'tallest_man_on_earth'
# URL = 'https://www.lyrics.com/artist/The-Tallest-Man-on-Earth/865422'


# get_lyrics_links(name, URL)
