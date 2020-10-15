import requests
import json
import os

def get_userdata():
    headers = { 'Authorization': 'Basic ' + os.getenv('API_KEY') }
    r = requests.get('http://uploader:3000/api/download', headers=headers)
    r.raise_for_status()
    return r.json()