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

def load_subscribers_id_list():
    subscribers_dict_list = load_subscribers()
    return [d["chat_id"] for d in subscribers_dict_list]

def find_subscriber_index(chat_id):
    dict_list = load_subscribers()
    index_generator = (index for (index, d) in enumerate(dict_list))
    print (list(index_generator))
    index_generator = (index for (index, d) in enumerate(dict_list) if d["chat_id"] == chat_id)
    return next(index_generator, None)

# Lista di utenti iscritti caricata dal file
save_subscribers([])
subscribers_dict_list = load_subscribers()
user_chat_ids=[d["chat_id"] for d in subscribers_dict_list]