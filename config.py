import os

API_TOKEN = os.environ.get("API_TOKEN", "placeholder")

DASHBOARD_HOSTNAME = os.environ.get("DASHBOARD_HOSTNAME", "placeholder")

TURNI_HOSTNAME = os.environ.get("TURNI_HOSTNAME", "placeholder")
TURNI_PORT = os.environ.get("TURNI_PORT", 8000)

MEALIE_HOSTNAME = os.environ.get("MEALIE_HOSTNAME", "placeholder")
MEALIE_PORT = os.environ.get("MEALIE_PORT", 8000)
MEALIE_TOKEN = os.environ.get("MEALIE_TOKEN", "placeholder")

SUBSCRIBERS_FILE = os.environ.get("SUBSCRIBERS_FILE", "placeholder")

HOME_ASSISTANT_HOSTNAME = os.environ.get("HOME_ASSISTANT_HOSTNAME","placeholder")
HOME_ASSISTANT_PORT = os.environ.get("HOME_ASSISTANT_PORT","8000")
HOME_ASSISTANT_TOKEN = os.environ.get("HOME_ASSISTANT_TOKEN","placeholder")
ID_LAVATRICE = os.environ.get("ID_LAVATRICE","placeholder")

SUBSCRIBERS_LAVATRICE_FILE = os.environ.get("SUBSCRIBERS_LAVATRICE_FILE", "placeholder")


flask_app_config = {
    "debug": os.environ.get("FLASK_DEBUG", True),
    "host": os.environ.get("FLASK_HOST", "0.0.0.0"),
    "port": os.environ.get("FLASK_PORT", 5000),
}

