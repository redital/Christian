import telebot
import funzioni
from config import *

import schedule
import subscribers
import time
from threading import Thread

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(API_TOKEN)

#================================================================================================================================================
#-------------------------------------------BASIC------------------------------------------------------------------------------------------------
#================================================================================================================================================

@bot.message_handler(commands=['start'])
def start_command(message):
   bot.send_message(
       message.chat.id,
       """
Ciao, io sono Christian il vero proprietario di casa Tassone e vi aiuterò nella vostra scellerata gestione domestica
       """
   )

@bot.message_handler(commands=['help'])
def start_command(message):
   bot.send_message(
       message.chat.id,
       """
I comandi sono:
/get_urls
/turni
/iscriviti
/disiscriviti
/lista_della_spesa
/svuota_lista_della_spesa
       """
   )

   

#================================================================================================================================================
#-------------------------------------------DASHBOARD URLS---------------------------------------------------------------------------------------
#================================================================================================================================================

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


#================================================================================================================================================
#-------------------------------------------TURNI------------------------------------------------------------------------------------------------
#================================================================================================================================================

@bot.message_handler(commands=['turni'])
def get_turni_delle_pulizie(message):
    msg = funzioni.genera_messaggio_turni(TURNI_HOSTNAME, TURNI_PORT)
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
    msg = funzioni.genera_messaggio_turni()
    for chat_id in subscribers.user_chat_ids:
        bot.send_message(chat_id, msg)

        

#================================================================================================================================================
#-------------------------------------------LISTA DELLA SPESA------------------------------------------------------------------------------------
#================================================================================================================================================


   
def gen_empty_list_markup(nome_lista):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Sì", callback_data="svuota lista della spesa si " + nome_lista),
        InlineKeyboardButton("No", callback_data="svuota lista della spesa no")
        )
    return markup

def gen_get_list_selection_markup(list_list):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    pulsanti = [InlineKeyboardButton(i, callback_data="lista da visualizzare : " + i) for i in list_list]
    markup.add(*pulsanti)
    return markup

def gen_empty_list_selection_markup(list_list):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    pulsanti = [InlineKeyboardButton(i, callback_data="lista da svuotare : " + i) for i in list_list]
    markup.add(*pulsanti)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,None)
    if "svuota lista della spesa si " in call.data :
        funzioni.empty_list(MEALIE_HOSTNAME, MEALIE_PORT,call.data.replace("svuota lista della spesa si ",""))
        bot.send_message(call.message.chat.id, "Lista svuotata")
    elif call.data == "svuota lista della spesa no":
        bot.send_message(call.message.chat.id, "Ok, non faccio nulla")
    elif "lista da visualizzare " in call.data :
        get_lista_della_spesa(call.message.chat.id, call.data.replace("lista da visualizzare : ",""))
    elif "lista da svuotare " in call.data :
        empty_lista_della_spesa_question(call.message, call.data.replace("lista da svuotare : ",""))

def domanda_empty_list(chat_id, nome_lista):
    bot.send_message(
        chat_id,
        "We, è passata un'ora da quando mi hai chiesto la lista della spesa, vuoi che la svuoti?",
        reply_markup=gen_empty_list_markup(nome_lista)
    )
    return schedule.CancelJob

@bot.message_handler(commands=['lista_della_spesa'])
def selezione_get_lista_della_spesa(message):
    list_list = funzioni.get_liste_della_spesa(MEALIE_HOSTNAME,MEALIE_PORT)
    bot.send_message(message.chat.id,"Quale lista vuoi vedere?",reply_markup=gen_get_list_selection_markup(list_list))
def get_lista_della_spesa(chat_id,nome_lista):
    msg = funzioni.genera_messaggio_lista_della_spesa(MEALIE_HOSTNAME, MEALIE_PORT,nome_lista)
    bot.send_message(chat_id,msg)
    schedule.every().hour.do(domanda_empty_list,chat_id=chat_id,nome_lista = nome_lista)

@bot.message_handler(commands=['svuota_lista_della_spesa'])
def selezione_empty_lista_della_spesa(message):
    list_list = funzioni.get_liste_della_spesa(MEALIE_HOSTNAME,MEALIE_PORT)
    bot.send_message(message.chat.id,"Quale lista vuoi svuotare?",reply_markup=gen_empty_list_selection_markup(list_list))
def empty_lista_della_spesa_question(message,nome_lista):
    bot.send_message(message.chat.id, "Vuoi che svuoti la lista della spesa?", reply_markup=gen_empty_list_markup(nome_lista))


#================================================================================================================================================
#-------------------------------------------LAVATRICE--------------------------------------------------------------------------------------------
#================================================================================================================================================


@bot.message_handler(commands=['stato_lavatrice'])
def get_stato_lavatrice(message):
    msg = funzioni.genera_messaggio_lavatrice(HOME_ASSISTANT_HOSTNAME, HOME_ASSISTANT_PORT)
    bot.send_message(
        message.chat.id,
        msg
    )

#================================================================================================================================================
#-------------------------------------------LOOP-------------------------------------------------------------------------------------------------
#================================================================================================================================================

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
    bot.infinity_polling()
