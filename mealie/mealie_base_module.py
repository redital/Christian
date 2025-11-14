import requests
import json
from config import * 
import random

api_token = MEALIE_TOKEN
mealie_url = "http://{}.local:{}".format(MEALIE_HOSTNAME,MEALIE_PORT)

def get_headers(token=mealie_url):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    return headers

