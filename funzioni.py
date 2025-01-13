from requests import get
import shopping_list
import socket

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

def get_turni_delle_pulizie(hostname, port):
    turni = get("http://{}:{}/stato_turni".format(get_local_ip(hostname),port))

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
    return ["lista 1", "lista 2","lista 3", "lista 4","lista 5", "lista 6","lista 7", "lista 8"]

def get_lista_della_spesa(hostname, port, nome_lista):
    return 

def genera_messaggio_lista_della_spesa(hostname, port, nome_lista):
    return "questa è la " + nome_lista 

def empty_list(hostname, port, nome_lista):
    return



