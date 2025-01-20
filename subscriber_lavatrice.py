from config import *
import json

# Funzione per caricare gli ID degli utenti iscritti
def load_subscribers():
    try:
        with open(SUBSCRIBERS_LAVATRICE_FILE, "r") as file:
            content = json.load(file)
            return content
    except FileNotFoundError:
        return []

# Funzione per salvare gli ID degli utenti iscritti
def save_subscribers(subscribers):
    with open(SUBSCRIBERS_LAVATRICE_FILE, "w") as file:
        json.dump(subscribers, file)

# Lista di utenti iscritti caricata dal file
save_subscribers([])
user_chat_ids = load_subscribers()