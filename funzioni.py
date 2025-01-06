from requests import get
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
    


#print(compute_urls("raffosberry"))
print(get_turni_delle_pulizie("workbanch", 8145))