from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "wasapbot123"
ACCESS_TOKEN = "EAAJpVDZAwkEABO7QgluI2m1UmIrOpdZBsIwTQyP5ATO0lnTO9FYhgnIORZAFwgoUyNT018FWFOsdTnhnR5ZAsdVMbkxddL6267sL1gv96oeZBOcmZCOKBDPZCVcOn3AEG7acxRXNlDNyNcjFZAZBIfzdjJHOJdCFDF2hlEfaBe9pTrZBTgMlZBUHkV7KE6ZA9I2ZBioSRa2JHCv7iT3Of22pdAF2s0dIaX2kh4eEFjHMZD"

@app.route('/')
def home():
    return 'Bot is running', 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("Received webhook:", data)

        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])

                    for message in messages:
                        phone_number_id = value["metadata"]["phone_number_id"]
                        from_number = message["from"]
                        msg_body = message["text"]["body"]

                        send_auto_reply(phone_number_id, from_number, msg_body)

        return "ok", 200

def send_auto_reply(phone_number_id, to, msg_body):
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {
            "body": f"👋 Hai! Kami telah terima mesej anda: \"{msg_body}\""
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print("Reply sent:", response.status_code, response.text)

if __name__ == '__main__':
    app.run(port=10000)
