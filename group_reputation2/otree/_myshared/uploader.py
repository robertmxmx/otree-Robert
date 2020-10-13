import requests
import json

def get_userdata():
    r = requests.get('http://uploader:3000/api/download')
    r.raise_for_status()
    return r.json()