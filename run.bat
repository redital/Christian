@echo off

rem Avvia il bot Telegram in background
start /B python main.py

rem Avvia l'app Flask
python flask_app.py

rem Mantenere la finestra aperta per vedere gli eventuali errori
pause
