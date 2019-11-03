from telethon import TelegramClient, events
import sys
from telethon.errors.rpcerrorlist import PeerIdInvalidError, PeerFloodError
import time

# Defining the need variables
api_id = '1036047' # Input your api_id here
api_hash = 'a0cc82720671666899cd30ddf100613c' # Input your api_hash here


## Connection of all the integrated APIs
client = TelegramClient("session", api_id, api_hash).start() # Starting Telegram Bot



async def send(user, msg, admin):

        try:
            if str(user) != '':
                user = await client.get_entity(str(user))
                try:
                    await client.send_message(user, f"{msg} --- Reply Unsub to cancel")
                    time.sleep(120)
                except PeerFloodError:
                    await client.send_message(admin.id, "This bot has been blocked and the software shut down. Restart the bot after 20 minutes!!!")
                    time.sleep(200)
                    await client.send_message(admin.id, "Bot Ready!!!")
                    return

        except PeerIdInvalidError:
            await client.send_message(admin.id, "User has blocked Wendy or has privacy on!!! Moving to next person")
            time.sleep(10)

        finally:
            return

    # msgs = await client.get_messages('Hutagg', limit=10)
    # for msg in msgs.data:
    #     if msg.media is not None:
    #         await client.download_media(message=msg)