import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# https://open.spotify.com/track/6zaKKRt9aMDO0uWxGI5ONc?si=3b505a0e83824a8d

# actual GET request with proper header
# r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

# r = r.json()

print(r)


if isinstance(access_token, str) == True:
    print(True)

# try:
#     r1 = requests.get(BASE_URL + 'me/top/artists/', headers=headers)
# except HTTPError as e:
#     if e.code == 403:
#         print('403 error')


# r1 = r1.json()

print(r1)