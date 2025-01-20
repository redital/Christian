import requests
from config import *

base_url = "/api/groups/shopping/lists"

ha_url = "http://{}.local:{}".format(HOME_ASSISTANT_HOSTNAME,HOME_ASSISTANT_PORT)
base_url = "/api/"

stati = {
    "0":"Idle",
    "1":"Lavaggio",
    "2":"?",
    "3":"Centrifuga",
}


def get_headers(HOME_ASSISTANT_TOKEN = HOME_ASSISTANT_TOKEN):
    headers = {
        "Authorization": "Bearer {}".format(HOME_ASSISTANT_TOKEN),
        "content-type": "application/json",
    }
    return headers

def get_stato_dispositivi(url = ha_url, HOME_ASSISTANT_TOKEN = HOME_ASSISTANT_TOKEN):
    response = requests.get("{}{}states".format(url,base_url) , headers=get_headers(HOME_ASSISTANT_TOKEN))
    return response.json()

def get_stato_lavatrice(url = ha_url, HOME_ASSISTANT_TOKEN = HOME_ASSISTANT_TOKEN, id_lavatrice = ID_LAVATRICE):
    return get_stato_dispositivo(id_lavatrice,url,HOME_ASSISTANT_TOKEN)["state"]
    
    
def get_stato_dispositivo(id_dispositivo, url = ha_url, HOME_ASSISTANT_TOKEN = HOME_ASSISTANT_TOKEN):
    response = requests.get("{}{}states/{}".format(url,base_url,id_dispositivo), headers=get_headers(HOME_ASSISTANT_TOKEN))
    return response.json()
    
def get_eventi(url = ha_url, HOME_ASSISTANT_TOKEN = HOME_ASSISTANT_TOKEN):
    response = requests.get("{}{}events".format(url,base_url), headers=get_headers(HOME_ASSISTANT_TOKEN))
    return response.json()
    
def get_servizi(url = ha_url, HOME_ASSISTANT_TOKEN = HOME_ASSISTANT_TOKEN):
    response = requests.get("{}{}services".format(url,base_url), headers=get_headers(HOME_ASSISTANT_TOKEN))
    return response.json()

