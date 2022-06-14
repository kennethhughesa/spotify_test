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

# headers = {
#     'Authorization': 'Bearer {token}'.format(token=access_token)
# }