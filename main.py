import telebot
import funzioni
from config import *


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


@bot.message_handler(commands=['canna'])
def get_turni_delle_pulizie(message):
   turni = funzioni.get_turni_delle_pulizie(TURNI_HOSTNAME,TURNI_PORT)
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
   bot.send_message(
       message.chat.id,
       msg
   )

@bot.message_handler(commands=['classifiche'])
def get_turni_delle_pulizie(message):
   msg = '\U00002757 This is a Robot face!\n'
   bot.send_message(
       message.chat.id,
       msg
   )


bot.polling()


