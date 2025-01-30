import telebot
import funzioni
from config import *

import schedule
import subscribers
import subscriber_lavatrice
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
    /start - start bot
    /help - info sul bot
    /get_urls - recupera url per la dashboard
    /turni - mostra i turni della settimana
    /iscriviti - iscrive la chat al servizio di notifica settimanale per i turni delle pulizie
    /disiscriviti - disiscrive la chat al servizio di notifica settimanale per i turni delle pulizie
    /lista_della_spesa - mostra una lista della spesa
    /svuota_lista_della_spesa - svuota una lista della spesa
    /stato_lavatrice - visualizza lo stato attuale della lavatrice
    /reminder_lavatrice - se la lavatrice è in funzione ti notificherà quando il ciclo sarà completato
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
    subscribers.user_chat_ids = subscribers.load_subscribers()
    if message.chat.id not in subscribers.user_chat_ids:
        subscribers.user_chat_ids.append(message.chat.id)
        subscribers.save_subscribers(subscribers.user_chat_ids)
        bot.send_message(message.chat.id, "Ti sei iscritto con successo al servizio di notifiche dei turni di pulizia!")
    else:
        bot.send_message(message.chat.id, "Sei già iscritto al servizio di notifiche.")

@bot.message_handler(commands=['disiscriviti'])
def disiscriviti(message):
    subscribers.user_chat_ids = subscribers.load_subscribers()
    if message.chat.id in subscribers.user_chat_ids:
        subscribers.user_chat_ids.remove(message.chat.id)
        subscribers.save_subscribers(subscribers.user_chat_ids)
        bot.send_message(message.chat.id, "Ti sei disiscritto con successo dal servizio di notifiche.")
    else:
        bot.send_message(message.chat.id, "Non risulti iscritto al servizio di notifiche.")


# Funzione per inviare il messaggio schedulato
def send_scheduled_turni():
    msg = funzioni.genera_messaggio_turni()
    subscribers.user_chat_ids = subscribers.load_subscribers()
    for chat_id in subscribers.user_chat_ids:
        bot.send_message(chat_id, msg)

        

#================================================================================================================================================
#-------------------------------------------LISTA DELLA SPESA------------------------------------------------------------------------------------
#================================================================================================================================================


   
def gen_empty_list_markup(nome_lista):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Svuota la lista", callback_data="svuota lista della spesa si " + nome_lista),
        InlineKeyboardButton("Non svuotare la lista", callback_data="svuota lista della spesa no")
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
    bot.send_message(chat_id,msg,reply_markup=gen_empty_list_markup(nome_lista))
    schedule.every().hour.do(domanda_empty_list,chat_id=chat_id,nome_lista = nome_lista).tag("lista_della_spesa" + str(chat_id) + nome_lista)

@bot.message_handler(commands=['svuota_lista_della_spesa'])
def selezione_empty_lista_della_spesa(message):
    list_list = funzioni.get_liste_della_spesa(MEALIE_HOSTNAME,MEALIE_PORT)
    bot.send_message(message.chat.id, "Quale lista vuoi svuotare?", reply_markup=gen_empty_list_selection_markup(list_list))
def empty_lista_della_spesa_question(message,nome_lista):
    bot.send_message(message.chat.id, "Vuoi che svuoti la lista della spesa?", reply_markup=gen_empty_list_markup(nome_lista))


#================================================================================================================================================
#-------------------------------------------LAVATRICE--------------------------------------------------------------------------------------------
#================================================================================================================================================


@bot.message_handler(commands=['stato_lavatrice'])
def get_stato_lavatrice(message):
    msg = funzioni.genera_messaggio_lavatrice(HOME_ASSISTANT_HOSTNAME, HOME_ASSISTANT_PORT)
    bot.send_message(message.chat.id,msg)

def gen_lavatrice_svuotata_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Sì", callback_data="lavatrice svuotata"),
        InlineKeyboardButton("No", callback_data="lavatrice non svuotata")
        )
    return markup

def gen_rompimi_il_cazzo_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Rompimi il cazzo", callback_data="lavatrice rompimi il cazzo"),
        )
    return markup

@bot.message_handler(commands=['reminder_lavatrice'])
def ricordami_di_scaricare_la_lavatrice(message):
    if funzioni.get_stato_lavatrice(HOME_ASSISTANT_HOSTNAME, HOME_ASSISTANT_PORT) == "0":
        bot.send_message(message.chat.id,"Vedi che la lavatrice non è in funzione")
        return
    subscriber_lavatrice.user_chat_ids = subscriber_lavatrice.load_subscribers()
    if message.chat.id in subscriber_lavatrice.user_chat_ids:
        bot.send_message(message.chat.id,"Sei già iscritto a questa notifica")
    else:
        subscriber_lavatrice.user_chat_ids.append(message.chat.id)
        subscriber_lavatrice.save_subscribers(subscriber_lavatrice.user_chat_ids)
        bot.send_message(message.chat.id,"Va bene, ti ricorderò di scaricare la lavatrice")


def notifica_lavatrice_finita():
    subscriber_lavatrice.user_chat_ids = subscriber_lavatrice.load_subscribers()
    for i in subscriber_lavatrice.user_chat_ids:
        bot.send_message(i,"Oh guarda che la lavatrice è finita")
        bot.send_message(i,"Vanno tolti presto i panni altrimenti puzzano",reply_markup=gen_rompimi_il_cazzo_markup())
    subscriber_lavatrice.user_chat_ids = []
    subscriber_lavatrice.save_subscribers(subscriber_lavatrice.user_chat_ids)


def lavatrice_svuotata(message):
    bot.send_message(message.chat.id,"Bravo ragazzo")
    schedule.clear("lavatrice")

def lavatrice_non_svuotata(message):
    bot.send_message(message.chat.id,"E forza su")


def domanda_lavatrice(chat_id):
    bot.send_message(chat_id,"Hai scaricato la lavatrice?", reply_markup = gen_lavatrice_svuotata_markup())


#================================================================================================================================================
#-------------------------------------------LOOP-------------------------------------------------------------------------------------------------
#================================================================================================================================================

# Loop per eseguire i task schedulati
def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

#================================================================================================================================================
#-------------------------------------------A CASO-----------------------------------------------------------------------------------------------
#================================================================================================================================================

        

@bot.message_handler(commands=['classifiche'])
def get_turni_delle_pulizie(message):
   msg = '\U00002757 This is a !\n'
   bot.send_message(
       message.chat.id,
       msg
   )

#================================================================================================================================================
#-------------------------------------------CALLBACK QUERY HANDLER-------------------------------------------------------------------------------
#================================================================================================================================================


   
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,None)
    if "svuota lista della spesa si " in call.data :
        nome_lista = call.data.replace("svuota lista della spesa si ","")
        funzioni.empty_list(MEALIE_HOSTNAME, MEALIE_PORT,nome_lista)
        schedule.clear("lista_della_spesa" + str(call.message.chat.id) + nome_lista)
        bot.send_message(call.message.chat.id, "Lista svuotata")
    elif call.data == "svuota lista della spesa no":
        bot.send_message(call.message.chat.id, "Ok, non faccio nulla")
    elif "lista da visualizzare " in call.data :
        get_lista_della_spesa(call.message.chat.id, call.data.replace("lista da visualizzare : ",""))
    elif "lista da svuotare " in call.data :
        empty_lista_della_spesa_question(call.message, call.data.replace("lista da svuotare : ",""))
    elif "lavatrice svuotata" in call.data :
        lavatrice_svuotata(call.message)
    elif "lavatrice non svuotata" in call.data :
        lavatrice_non_svuotata(call.message)
    elif "lavatrice rompimi il cazzo" in call.data :
        schedule.every(15).minutes.do(domanda_lavatrice,chat_id=call.message.chat.id).tag("lavatrice",call.message.chat.id)

        

#================================================================================================================================================
#-------------------------------------------RUN--------------------------------------------------------------------------------------------------
#================================================================================================================================================


def scheduler_initialize():
    # Programmare il messaggio ogni sabato alle 9
    schedule.every().saturday.at("09:00").do(send_scheduled_turni)
    # Avvia lo scheduler in un thread separato
    Thread(target=scheduler_loop).start()

# Avviare il polling e lo scheduler
if __name__ == "__main__":
    scheduler_initialize()
    # Avvia il polling del bot
    bot.infinity_polling()
