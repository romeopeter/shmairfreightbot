from flask import Flask, request
from decouple import config

app = Flask(__name__)


@app.route("/easypost-webhook", method=["post"])
def process_webhook():

    request = request.get_json()

    # Check if wehbook is about tracker event
    # If key of 'object' has 'Event' and key 'description' has 'tracker.updated' then it is a tracker event


# NOTE: Ngrok not exposing local web server
# Error message: listen tcp 127.0.0.1:4049: bind: An attempt was made to access a socket in a way forbidden by its access permissions.
