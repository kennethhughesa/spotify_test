import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
import webbrowser
import base64
from urllib.parse import urlencode

load_dotenv()

class spotify_request:
    def __init__(self, client_id, client_secret):
        self.client_id = os.environ.get(client_id)
        self.client_secret = os.environ.get(client_secret)

client = spotify_request('Spotify_Client_ID', 'Spotify_Client_Secret')

SPOTIFY_REDIRECT_URI = 'http://localhost:3000/callback'

def authorize_scope(client_id, client_secret, SPOTIFY_REDIRECT_URI):
    scopes = 'user-read-recently-played'
    scopes_auth_headers = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "scope": scopes
    }
    
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(scopes_auth_headers), new=2)


def get_token(client_id, client_secret):
    token_auth_url = 'https://accounts.spotify.com/api/token'

    token_headers = {
        'grant_type': 'client_credentials',
        'client_id': client.client_id,
        'client_secret': client.client_secret,
    }

    auth_response = requests.post(token_auth_url, token_headers )

    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    # configure header object for access to resource
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    code = input('paste code from end of url here:')

    return access_token, headers

def get_data(access_token, headers):
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # https://open.spotify.com/track/6zaKKRt9aMDO0uWxGI5ONc?si=3b505a0e83824a8d

    # actual GET request with proper header
    # r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

    track_id = '6zaKKRt9aMDO0uWxGI5ONc' 
    scopes = 'user-read-recently-played'


    if isinstance(access_token, str) == True:
        print('----- token string received, attempting to retrieve data...  -----')

        try:
            response = requests.get(BASE_URL + 'me/top/artists', headers=headers)
            # response = requests.get(f'https://accounts.spotify.com/authorize?client_id={client.client_id}&response_type=code&redirect_uri=http%3A%2F%2Flocalhost:3000%2Fcallback&scope={scopes}')
            # response = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
            response.raise_for_status()
            print('----- data retrieved -----')
            print(response)
            return response.content
        except requests.HTTPError as error:
            print('Error returned:\n', error)
            return None
        except requests.exceptions.RequestException as e:
            print("Connection refused", e)
            return None
        except Exception as e:
            print("Internal error", e)
            return None

        print('----- converting data...  -----')
        
        try:
            body = response.content

            if response.text:
                print('response is text')
                print(body)
        except ValueError:
            print('----- no text returned -----')

        try:
            json_data = response.json()
            
            if json_data:
                print('----- response is JSON -----')
                print(json_data)
        except ValueError:
            # no JSON returned
            print('----- no JSON returned -----')




    # r1 = r1.json()

    print(response)

if __name__ == "__main__":
    spotify_request
    authorize_scope(client.client_id, client.client_secret, SPOTIFY_REDIRECT_URI)
    access_token, headers = get_token(client.client_id, client.client_secret)
    get_data(access_token, headers)
