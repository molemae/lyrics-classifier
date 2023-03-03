from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



# Click on the search button of the lyrics.com website
def search_on_chrome(artist_name, url):
    print(f'Artist name to be searched for : {artist_name}')

    
    # Set the Chrome Web Driver path
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome-beta"
    driver = webdriver.Chrome(options=chrome_options, service = Service(ChromeDriverManager().install()))
    
    # Ask the driver to get the url
    driver.get(url)

    # Wait
    wait = WebDriverWait(driver,20)

    # Click on Consent
    try:
        cookie = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="s4-page-homepage"]/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]/p')))
        cookie.click()                                              # //*[@id="s4-page-homepage"]/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]/p
        print('Clicked on consent')                                 #//*[@id="s4-page-homepage"]/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]/p
    except:
        print("Couldn't find the consent page")                      # //*[@id="s4-page-homepage"]/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]/p
    
    # Time Sleep
    time.sleep(5)
    try:
        # Find the search button
        search = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]')))
        search.send_keys(artist_name)                                          
        # Send the entered artist name
        search.send_keys(Keys.RETURN) # hit return after you enter search text        
        print('Found the artist')
    except:
        print('Search element not visible')
    
    # Wait
    time.sleep(10)

    current_url = driver.current_url

    driver.close()

    return current_url


def get_artist_url(artist_name, url):
    # Get the list of artists named with artist_name
    url_for_response = search_on_chrome(artist_name, url)

    # Send request to the url 
    response = requests.get(url = url_for_response)
    response_text = response.text

    # Parse content into html 
    parsed_content = BeautifulSoup(markup = response_text, features = 'html.parser')

    # Get the link of the artist page
    link = (parsed_content.find('a', attrs = {'title':artist_name})).get('href')

    return ("https://www.lyrics.com/" + link)


def store_link_in_list(url, *list_of_artists):

    # Print the list of artists
    print(f'List of artists given as input : {list_of_artists}')

    # Create a empty list of artists
    artists = []

    # Create an empty list of links to the artist pages
    artist_links = []

    # Loop through the list of artists
    for artist_name in list_of_artists:
        print(f'Artist name to be sent for searching for : {artist_name}')

        # Get the link to the Artist page
        artist_link = get_artist_url(artist_name=artist_name, url = url)
        print(f'Link of all the songs of the artist: {artist_link}')

        # Append artists with artist_name
        artists.append(artist_name)

        # Append artist_links with the links
        artist_links.append(artist_link)
    
    print(f'The list containing the artist song links: {artist_links}')
    print(f'The list containing the artist song links: {artists}')

    # Create a dictionary with artist names and artist links    
    names_links = zip(artists, artist_links)

    return names_links


# store_link_in_list('http://www.lyrics.com', 'Adele', 'Taylor Swift')