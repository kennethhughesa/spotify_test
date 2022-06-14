import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# auth request class
class spotify_request:
    def __init__(self, client_id, client_secret):
        self.client_id = os.environ.get(client_id)
        self.client_secret = os.environ.get(client_secret)

# initialize class and pass environment variables into class to create attributes for client object
client = spotify_request('Spotify_Client_ID', 'Spotify_Client_Secret')

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
if ((client.client_id != np.NaN) and (client.client_secret != np.NaN)):
    try:
        auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        })
    except HTTPError as e:
        if e.code == 403:
            print('403 error')

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
try:
    access_token = auth_response_data['access_token']
except token_error as e:
    print('no token exists')

# configure header object for access to resource
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

