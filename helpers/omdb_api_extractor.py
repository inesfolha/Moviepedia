import json
from dotenv import load_dotenv
import os
import requests
from colorama import Fore, init
load_dotenv()
init()

API_KEY = os.getenv("API_KEY")
URL = f'http://www.omdbapi.com/?i=tt3896198&apikey={API_KEY}'


def data_extractor(movie):
    try:
        response = requests.get(f'http://www.omdbapi.com/?i=tt3896198&apikey={API_KEY}&t={movie}')
        response.raise_for_status()  # raise an exception if the response status code is not 200 OK
        data_result = response.json()
        return data_result
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "An error occurred while trying to access the API:", e, Fore.RESET)
        return None


def get_imdb_link(title):
    # Make a request to the OMDb API
    response = requests.get(f'http://www.omdbapi.com/?apikey={API_KEY}&t={title}')

    # Parse the JSON response
    data = json.loads(response.text)

    # Extract the IMDb link
    imdb_id = data.get('imdbID')
    imdb_link = f'https://www.imdb.com/title/{imdb_id}/'

    return imdb_link
