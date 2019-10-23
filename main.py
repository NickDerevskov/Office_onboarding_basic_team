from dialog_bot_sdk.bot import DialogBot
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

#TODO
def send_guides(id, peer):
    bot.messaging.send_message(peer, 'Sending guides')

def auth(id, peer):
    if is_exist(id):
        send_manager_buttons(id, peer) if is_manager(id) else send_guides(id, peer) 
    else:
        #TODO WORK WITH TOKEN
        bot.messaging.send_message('You are not sing in')

# Main fun
def main(*params):
    id = params[0].peer.id
    peer = params[0].peer

    bot.messaging.send_message(peer, 'Hey')
    auth(id, peer)
    

if __name__ == "__main__":
    bot = DialogBot.get_secure_bot(
        "hackathon-mob.transmit.im",  # bot endpoint (specify different endpoint if you want to connect to your on-premise environment)
        grpc.ssl_channel_credentials(),  # SSL credentials (empty by default!)
        bot_token,  # bot token
        verbose=False,  # optional parameter, when it's True bot prints info about the called methods, False by default
    )

# work like return , block code after, if want to use code after, use async vers
bot.messaging.on_message(main)
