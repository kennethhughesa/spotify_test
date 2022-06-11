import pandas as pd
import requests
import os

class spotify_request:
    def __init__(self, client_id):
        self.CLIENT_ID = os.environ.get(client_id)


client = spotify_request('Spotify_Client_ID')

print(client.CLIENT_ID)