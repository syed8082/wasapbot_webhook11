from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "wasapbot123")  # Token custom anda

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "Forbidden", 403

    elif request.method == "POST":
        data = request.get_json()
        print("Received webhook POST:", data)
        return "EVENT_RECEIVED", 200

    else:
        return "Method Not Allowed", 405

@app.route("/")
def index():
    return "WhatsApp Bot Webhook is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)