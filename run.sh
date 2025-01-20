#!/bin/bash

# Avvia il bot Telegram in background
python main.py &

# Avvia l'app Flask
python flask_app.py
