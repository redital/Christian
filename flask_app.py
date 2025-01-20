from flask import Flask, request, jsonify
from main import notifica_lavatrice_finita, scheduler_initialize, bot
from threading import Thread
from config import *

# Crea un server Flask
app = Flask(__name__)

# Memorizza lo stato dei messaggi inviati
sent_messages = []

@app.route('/notifica_lavatrice', methods=['GET'])
def send_message():
    
    notifica_lavatrice_finita()

    return jsonify({"status": "success", "message": "Messaggio inviato"}), 200

def flask_initializer():
    Thread(target=app.run,kwargs=flask_app_config).start()

if __name__ == "__main__":
    scheduler_initialize()
    Thread(target=bot.infinity_polling,daemon=True).start
    app.run(**flask_app_config)
    #flask_initializer()
    # Avvia il polling del bot
    #bot.infinity_polling()