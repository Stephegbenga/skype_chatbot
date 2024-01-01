import json, requests
from config import bot_id, api_key, app_id, app_secret
base_url = "https://api.50chats.com/api"
import time




class SimpleCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            value, expiry_time = self.cache[key]
            if expiry_time is None or time.time() < expiry_time:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key, value, expiry_seconds=None):
        expiry_time = None
        if expiry_seconds is not None:
            expiry_time = time.time() + expiry_seconds
        self.cache[key] = (value, expiry_time)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]


Local_Cache = SimpleCache()



def get_reply(contact_id, text_message, name):
    payload = {"contact_id": contact_id, "text":text_message, "bot_id": bot_id,
               "full_name":name}


    headers = {'Content-Type': 'application/json', 'api_key': api_key}
    url = f"{base_url}/message/send"

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload)).json()
    return response


def get_token():
    token = Local_Cache.get("token")
    if token:
        return token

    payload = "grant_type=client_credentials&client_id=" + app_id + "&client_secret=" + app_secret + "&scope=https%3A%2F%2Fapi.botframework.com%2F.default"
    response = requests.post(
        "https://login.microsoftonline.com/common/oauth2/v2.0/token?client_id=" + app_id + "&client_secret=" + app_secret + "&grant_type=client_credentials&"
                                                                                                                                  "scope=https%3A%2F%2Fgraph.microsoft.com%2F.default",
        data=payload,
        headers={"Host": "login.microsoftonline.com", "Content-Type": "application/x-www-form-urlencoded"})
    data = response.json()
    token = data["access_token"]
    Local_Cache.set("token", token, 3590)
    return token