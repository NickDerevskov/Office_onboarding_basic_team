from dialog_bot_sdk.bot import DialogBot
from dialog_bot_sdk import interactive_media
from pymongo import MongoClient
import grpc
import time

# Utils
client = MongoClient("mongodb://team:123ert@ds018839.mlab.com:18839/new_hackaton", retryWrites= False)
db = client.new_hackaton
reviews = db.reviews
bot_token = '4a3a998e50c55e13fb4ef9a52a224303602da6af'
# https://github.com/dialogs/chatbot-hackathon - basic things
# https://hackathon.transmit.im/web/#/im/u2108492517 - bot

def is_exist(id):
    return False if reviews.find_one({"id":id}) is None else True

def is_manager(id):
    return True if reviews.find_one({"id":id})['name'] == "Office-manager" else False

#TODO
def send_manager_buttons(id, peer):
    bot.messaging.send_message(peer, 'Sending manager buttons')

    buttons = [interactive_media.InteractiveMediaGroup(
            [
                interactive_media.InteractiveMedia(
                    1,
                    interactive_media.InteractiveMediaButton('add', "Add guide"),
                ),
                interactive_media.InteractiveMedia(
                    150,
                    interactive_media.InteractiveMediaButton("get_token", "Get token")
                ),
            ]
        )]

    bot.messaging.send_message(peer, "Choose option", buttons)

#TODO
def send_guides(id, peer):
    bot.messaging.send_message(peer, 'Sending guides')

    buttons = [interactive_media.InteractiveMediaGroup(
            [
                interactive_media.InteractiveMedia(
                    2,
                    interactive_media.InteractiveMediaButton('kitchen', "Guide about kitchen"),
                ),
                interactive_media.InteractiveMedia(
                    3,
                    interactive_media.InteractiveMediaButton("wifi", "Guide about wifi")
                ),
            ]
        )]

    bot.messaging.send_message(peer,"Choose guide", buttons)

def auth(id, peer):
    if is_exist(id):
        send_manager_buttons(id, peer) if is_manager(id) else send_guides(id, peer) 
    else:
        #TODO WORK WITH TOKEN
        bot.messaging.send_message(peer, 'You are not sing in')

def start_text(peer):
    bot.messaging.send_message(peer, 'This is start message')

# Main fun
def main(*params):
    id = params[0].peer.id
    peer = params[0].peer

    bot.messaging.send_message(peer, 'Hey')

    if params[0].message.textMessage.text == "/start":
        start_text(peer)

    time.sleep(2) # for better usage
    auth(id, peer)

def on_click(*params):
    id = params[0].uid
    value = params[0].value
    print(params)
    peer = bot.users.get_user_peer_by_id(id)

    bot.messaging.send_message(peer, 'you click button ' + value)    

if __name__ == "__main__":
    bot = DialogBot.get_secure_bot(
        "hackathon-mob.transmit.im",  # bot endpoint (specify different endpoint if you want to connect to your on-premise environment)
        grpc.ssl_channel_credentials(),  # SSL credentials (empty by default!)
        bot_token,  # bot token
        verbose=False,  # optional parameter, when it's True bot prints info about the called methods, False by default
    )

# work like return , block code after, if want to use code after, use async vers
bot.messaging.on_message(main, on_click)
