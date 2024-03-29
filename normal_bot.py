from skype_chatbot import send_message
import json
from flask import Flask, request
from util import get_reply
from config import app_id, app_secret


app = Flask(__name__)



@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    req = request.json
    print(req)
    return "received"



@app.route('/api/messages', methods=['POST', 'GET'])
def api_messages():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            text_message = data.get("text")
            user_name = data['from'].get("name")
            contact_id = data['conversation']['id']


            response = get_reply(contact_id, text_message, user_name)
            responses = response['data']

            for response in responses:
                print(response)
                reply_text = response['raw_message']['message']

                bot_id = data['recipient']['id']
                bot_name = data['recipient']['name']
                recipient = data['from']
                service = data['serviceUrl']
                sender = data['conversation']['id']
                text = reply_text

                send_message(bot_id, bot_name, recipient, service, sender, text, 'markdown')

        except Exception as e:
            print(e)

    return 'Code: 200'


if __name__ == '__main__':
    app.run()