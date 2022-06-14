import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class spotify_request:
    def __init__(self, client_id, client_secret):
        self.client_id = os.environ.get(client_id)
        self.client_secret = os.environ.get(client_secret)

client = spotify_request('Spotify_Client_ID', 'Spotify_Client_Secret')


AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client.client_id,
    'client_secret': client.client_secret,
})

# convert the response to JSON
auth_response_data = auth_response.json()

print(auth_response_data)

# save the access token
access_token = auth_response_data['access_token']

# configure header object for access to resource
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# https://open.spotify.com/track/6zaKKRt9aMDO0uWxGI5ONc?si=3b505a0e83824a8d

# actual GET request with proper header
# r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

# r = r.json()

# print(r)


if isinstance(access_token, str) == True:
    print(True)
    print(BASE_URL)
    print(headers)

try:
    r1 = requests.get(BASE_URL + 'me/top/artists', headers=headers)
except HTTPError as e:
    if e.code == 403:
        print('403 error')


# r1 = r1.json()

print(r1)