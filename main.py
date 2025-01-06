import telebot
import funzioni
from config import *

import schedule
import subscribers
import time
from threading import Thread

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
   bot.send_message(
       message.chat.id,
       """
Ciao, io sono Christian il vero proprietario di casa Tassone e vi aiuterò nella vostra scellerata gestione domestica
       """
   )

@bot.message_handler(commands=['get_urls'])
def get_urls(message):
   urls = funzioni.compute_urls(DASHBOARD_HOSTNAME)
   bot.send_message(
       message.chat.id,
       """
Puoi accedere alla dashboard domestica e a tutti i suoi servizi se sei collegato alla rete locale tramite i seguenti link:
       
    hostname : {hostname}
    local_ip : {local_ip}

Oppure dal web in sola visualizzazione al seguente link:

    public_ip : {public_ip}
       """.format(**urls)
   )

def genera_messaggio_turni():
    turni = funzioni.get_turni_delle_pulizie(TURNI_HOSTNAME, TURNI_PORT)
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

@bot.message_handler(commands=['turni'])
def get_turni_delle_pulizie(message):
    msg = genera_messaggio_turni()
    bot.send_message(
        message.chat.id,
        msg
    )

@bot.message_handler(commands=['iscriviti'])
def iscriviti(message):
    if message.chat.id not in subscribers.user_chat_ids:
        subscribers.user_chat_ids.append(message.chat.id)
        subscribers.save_subscribers(subscribers.user_chat_ids)
        bot.send_message(message.chat.id, "Ti sei iscritto con successo al servizio di notifiche dei turni di pulizia!")
    else:
        bot.send_message(message.chat.id, "Sei già iscritto al servizio di notifiche.")

@bot.message_handler(commands=['disiscriviti'])
def disiscriviti(message):
    if message.chat.id in subscribers.user_chat_ids:
        subscribers.user_chat_ids.remove(message.chat.id)
        subscribers.save_subscribers(subscribers.user_chat_ids)
        bot.send_message(message.chat.id, "Ti sei disiscritto con successo dal servizio di notifiche.")
    else:
        bot.send_message(message.chat.id, "Non risulti iscritto al servizio di notifiche.")


# Funzione per inviare il messaggio schedulato
def send_scheduled_turni():
    msg = genera_messaggio_turni()
    for chat_id in subscribers.user_chat_ids:
        bot.send_message(chat_id, msg)


# Loop per eseguire i task schedulati
def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

        

@bot.message_handler(commands=['classifiche'])
def get_turni_delle_pulizie(message):
   msg = '\U00002757 This is a Robot face!\n'
   bot.send_message(
       message.chat.id,
       msg
   )

# Avviare il polling e lo scheduler
if __name__ == "__main__":
    # Programmare il messaggio ogni sabato alle 9
    schedule.every().saturday.at("09:00").do(send_scheduled_turni)
    # Avvia lo scheduler in un thread separato
    Thread(target=scheduler_loop).start()
    # Avvia il polling del bot
    bot.polling()
