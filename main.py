from dialog_bot_sdk.bot import DialogBot
import grpc


def on_msg(*params):
    print('on msg', params)
    bot.messaging.send_message(
        params[0].peer, 'Reply to : ' + str(params[0].message.textMessage.text)
    )


if __name__ == '__main__':
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im',  # bot endpoint (specify different endpoint if you want to connect to your on-premise environment)
        grpc.ssl_channel_credentials(), # SSL credentials (empty by default!)
        '4a3a998e50c55e13fb4ef9a52a224303602da6af',  # bot token
        verbose=True # optional parameter, when it's True bot prints info about the called methods, False by default
    )

    bot.messaging.on_message(on_msg)