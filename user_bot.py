from skpy import SkypeEventLoop, SkypeNewMessageEvent
from flask import Flask, request
from util import get_reply
from config import app_id, app_secret, username, password
from threading import Thread


app = Flask(__name__)



class SkypePing(SkypeEventLoop):
    def __init__(self):
        super(SkypePing, self).__init__(username, password, "login.txt")
    def onEvent(self, event):
        try:
            sender_id = None
            sender_name = None

            try:
                sender_name = event.user.name
            except Exception as e:
                pass



            try:
                if not sender_name:
                    sender_name = event.msg.chat.getContact(sender_id).name
            except Exception as e:
                pass

            if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
                sender_id = event.msg.userId
                message = event.msg.plain
                if not sender_id:
                    return

                response = get_reply(sender_id, message, sender_name)
                responses = response['data']

                for response in responses:
                    reply_text = response['raw_message']['message']

                    event.msg.chat.sendMsg(reply_text)
        except Exception as e:
            print(e)
            pass


def start_message_listener():
    skype_ping = SkypePing()
    skype_ping.loop()

if __name__ == '__main__':
    Thread(target=start_message_listener).start()
    app.run()