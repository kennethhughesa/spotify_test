import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv
import webbrowser
import base64
from urllib.parse import urlencode

# read me for auth flow
# 1. create spotify dev account
# 2. add user you wish to get data for to USERS AND ACCESS
# 3. add redirect uri in EDIT SETTINGS
# 4. get auth code after user authorizes access to data
# 5. get auth token
# 6. get data



load_dotenv()

class spotify_request:
    def __init__(self, client_id, client_secret):
        self.client_id = os.environ.get(client_id)
        self.client_secret = os.environ.get(client_secret)

client = spotify_request('Spotify_Client_ID', 'Spotify_Client_Secret')

SPOTIFY_REDIRECT_URI = 'http://localhost:3000/callback'

def get_auth_code(client_id, client_secret, SPOTIFY_REDIRECT_URI):
    scopes = 'user-read-recently-played'
    scopes_auth_headers = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "scope": scopes,
            "show_dialog": "true"
    }
    
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(scopes_auth_headers), new=2)

    auth_code = input('paste code from end of url here:')

    return auth_code

def get_auth_token(client_id, client_secret, SPOTIFY_REDIRECT_URI, auth_code):
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
    token_auth_url = 'https://accounts.spotify.com/api/token'

    token_headers = {
        'Authorization': 'Basic ' + encoded_credentials,
        'Content-Type': 'application/x-www-form-urlencoded'        
        
        # token headers if requesting non-user data 
        # 'grant_type': 'client_credentials',
        # 'client_id': client.client_id,
        # 'client_secret': client.client_secret,
    }

    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': SPOTIFY_REDIRECT_URI
    }

    r = requests.post(token_auth_url, data=token_data, headers=token_headers)

    token = r.json()['access_token']


    # code for getting non user data 
    # auth_response = requests.post(token_auth_url, token_headers )

    # auth_response_data = auth_response.json()

    # save the access token
    # access_token = auth_response_data['access_token']

    # configure header object for access to resource
    # headers = {
    #     'Authorization': 'Bearer {token}'.format(token=access_token)
    # }

    return token

def get_data(token):
    # base URL of all Spotify API endpoints
    # BASE_URL = 'https://api.spotify.com/v1/me/player/recently-played'
    BASE_URL = 'https://api.spotify.com/v1/users/Tiffanyhughes48/playlists'

    # code for getting track data/ non user data
    # actual GET request with proper header
    # track_id = '6zaKKRt9aMDO0uWxGI5ONc' 
    # r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

    user_headers = {
        'Authorization': 'Bearer {token}'.format(token=token),
        'Content-Type': 'application/json',
        'client_id': client.client_id,
        'client_secret': client.client_secret
    }

    user_params = {
        'after': 1656048878,
        'limit': 50
    }

    if isinstance(token, str) == True:
        print('----- token string received, attempting to retrieve data...  -----')

        try:
            response = requests.get(BASE_URL, params=user_params, headers=user_headers)
            # response = requests.get(f'https://accounts.spotify.com/authorize?client_id={client.client_id}&response_type=code&redirect_uri=http%3A%2F%2Flocalhost:3000%2Fcallback&scope={scopes}')
            # response = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
            response.raise_for_status()
            print('----- data retrieved -----')
            print(f'response object is: {response}')
            print(f'response object content is: {response.content}')
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
    auth_code = get_auth_code(client.client_id, client.client_secret, SPOTIFY_REDIRECT_URI)
    token = get_auth_token(client.client_id, client.client_secret, SPOTIFY_REDIRECT_URI, auth_code)
    get_data(token)
