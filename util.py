import json, requests
from config import bot_id, api_key
base_url = "https://api.50chats.com/api"



def get_reply(contact_id, text_message, name):
    payload = {"contact_id": contact_id, "text":text_message, "bot_id": bot_id,
               "full_name":name}


    headers = {'Content-Type': 'application/json', 'api_key': api_key}
    url = f"{base_url}/message/send"

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload)).json()
    return response


