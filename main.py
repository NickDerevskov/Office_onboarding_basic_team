from dialog_bot_sdk.bot import DialogBot
from pymongo import MongoClient
import grpc
import time

# Utils
client = MongoClient(port=27017)
db = client.onboarding
is_first_message = False


def on_msg(msg, *params):
    print("on msg", params)
    bot.messaging.send_message(params[0].peer, msg)


# Add data to db
def add_user_to_admins(id):
    db.reviews.insert_one({"name": "Office-manager", "id": id})


# Main fun
def main(*params):
    global is_first_message
    on_msg("Hello user", *params)

    if is_first_message == False:
        add_user_to_admins(params[0].peer.id)
        bot.messaging.send_message(params[0].peer, "You became a office manager!")
        is_first_message = True
        return is_first_message

    time.sleep(2)  # to better usage
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
