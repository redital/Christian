from requests import get
import shopping_list
import socket
import home_assisstant

def get_local_ip(hostname):
    ips=[i[4][0] for i in socket.getaddrinfo(hostname, None) if i[0] == 2]
    return ips[0]

def get_public_ip():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return ip

def compute_urls(hostname):
    res = {
        "hostname":"http://{}.local".format(hostname),
        "local_ip":"http://{}".format(get_local_ip(hostname)),
        "public_ip":"http://{}".format(get_public_ip()),
    }
    return res

def get_service_url(hostname, port):
    return "http://{}:{}".format(get_local_ip(hostname),port)

def get_turni_delle_pulizie(hostname, port):
    turni_url = get_service_url(hostname,port)
    turni = get("{}/stato_turni".format(turni_url))
    return turni.json()

def genera_messaggio_turni(hostname, port):
    turni = get_turni_delle_pulizie(hostname, port)
    for i in turni:
        if i["completato"]:
            i["completato"] = "\U00002705"
        else:
            i["completato"] = "\U00002757"
        if i["compito"] == "Riposo":
            i["completato"] = "\U0001F929"
    msg = ""
    for i in turni:
        msg += "\n{nome} - {compito}  {completato}".format(**i)
    return msg    

def get_liste_della_spesa(hostname, port):
    mealie_url = get_service_url(hostname,port)
    shopping_list.update_shopping_lists(api_url=mealie_url)
    return list(shopping_list.shopping_lists.keys())

def get_lista_della_spesa(hostname, port, nome_lista):
    mealie_url = get_service_url(hostname,port)
    id_lista = shopping_list.shopping_lists[nome_lista]
    json_data = shopping_list.get_shopping_list(item_id=id_lista,api_url=mealie_url)
    return [i["display"] for i in json_data["listItems"]]
    

def genera_messaggio_lista_della_spesa(hostname, port, nome_lista):
    msg = "Questa è la lista" + nome_lista + ":\n"
    for i in get_lista_della_spesa(hostname, port, nome_lista):
        msg += "-" + i + "\n"
    return msg

def empty_list(hostname, port, nome_lista):
    mealie_url = get_service_url(hostname,port)
    id_lista = shopping_list.shopping_lists[nome_lista]
    shopping_list.empty_list(item_id=id_lista,api_url=mealie_url)
    return



def genera_messaggio_lavatrice(hostname, port):
    ha_url = get_service_url(hostname, port)
    stato = home_assisstant.get_stato_lavatrice(url=ha_url)
    msg = "Ciao, sono Christian la lavatrice e il mio stato in questo momento è: {}".format(home_assisstant.stati[stato])
    return msg    
