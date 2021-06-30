import requests
from pprint import pprint
regions = ['in'] # Change to your country
with open('Demo_images/IMG_8308.jpeg', 'rb') as fp:
    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        data=dict(regions=regions),  # Optional
        files=dict(upload=fp),
        headers={'Authorization': 'Token ec549d56a1930e6da1cbe3dccda9910bcb54072a'})
resp = response.json()

Plate = str(resp['results'][0]['plate']).upper()

