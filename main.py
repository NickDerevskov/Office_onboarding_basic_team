from dialog_bot_sdk.bot import DialogBot
from pymongo import MongoClient
import grpc
import time

# Utils
client = MongoClient("mongodb://team:123ert@ds018839.mlab.com:18839/new_hackaton", retryWrites= False)
db = client.new_hackaton
reviews = db.reviews
# https://github.com/dialogs/chatbot-hackathon - basic things
# https://hackathon.transmit.im/web/#/im/u2108492517 - bot

def on_msg(msg, *params):
    #print("on msg", params)
    #print("\n--------------------------------------------")
    bot.messaging.send_message(params[0].peer, msg)


# Add data to db
def add_user_to_admins(id):
    reviews.insert_one({"name": "Office-manager", "id": id})


def is_first_message(id):
    return True if reviews.find_one({"id":id}) is None else False


def is_admin(id):
    return False if reviews.find_one({"id":id})['name'] != "Office-manager" else True


# Main fun
def main(*params):
    id = params[0].peer.id
    user = bot.users.get_user_by_id(id)
    on_msg("Hello user "+user.data.name, *params)

    if (is_first_message(id) == True):
        add_user_to_admins(id)
        bot.messaging.send_message(params[0].peer, "You became a office manager!")
        return

    if (is_admin(id) == True):
        bot.messaging.send_message(params[0].peer, "You are a office manager!")
        return
    #time.sleep(2)  # to better usage
    on_msg("It is not first message!", *params)


if __name__ == "__main__":
    bot = DialogBot.get_secure_bot(
        "hackathon-mob.transmit.im",  # bot endpoint (specify different endpoint if you want to connect to your on-premise environment)
        grpc.ssl_channel_credentials(),  # SSL credentials (empty by default!)
        "4a3a998e50c55e13fb4ef9a52a224303602da6af",  # bot token
        verbose=False,  # optional parameter, when it's True bot prints info about the called methods, False by default
    )

# work like return , block code after, if want to use code after, use async vers
bot.messaging.on_message(main)
