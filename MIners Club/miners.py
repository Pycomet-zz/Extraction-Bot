import telebot
from telethon import TelegramClient, sync, events
import time

## Defining the need variables
api_id = '683428' # Input your api_id here
api_hash = '967b28d111f82b906b6f28da1ff04411' # Input your api_hash here

token = '927041875:AAHr9CfWRwJhXMArxIwwyjLL12es8DI62VI'

admin = [577180091]

## Connection of all the integrated APIs
bot = TelegramClient("Hack", api_id, api_hash)
bot.start()

name = input("Enter the link to the group here: ")

channel = bot.get_entity(name)

members = bot.get_participants(channel)

chat = bot.get_entity("https://t.me/minershu")

[bot.send_message(chat, f"{each.username}") for each in members if each.username is not None and each.bot is False]

print("Bot running!!!")
bot.run_until_disconnected()
while True:
    pass