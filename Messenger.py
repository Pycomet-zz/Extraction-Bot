############################################################################################################################################################################
############################################################################################################################################################################

## This code was written by Codefred
## Compactible with Python3 Interpreter

############################################################################################################################################################################
############################################################################################################################################################################

## This script sends custom messages to User.csv file

# https://dry-scrubland-17857.herokuapp.com/ | https://git.heroku.com/dry-scrubland-17857.git  ## Heroku Access

############################################################################################################################################################################

# Importing necessary libraries
import telebot
from telebot import types
from telethon import TelegramClient, events
from pprint import pprint
import logging
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import pandas
import requests
import sender
import asyncio
loop = asyncio.get_event_loop()

# Setup Logging
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="messenger.log", format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
#
# ## Defining the need variables
# api_id = '761526' # Input your api_id here
# api_hash = '71ec605bc89cc9f7d755d3e3fe5798d1' # Input your api_hash here # Input your api_hash here


# Defining the need variables
api_id = '683428' # Input your api_id here
api_hash = '967b28d111f82b906b6f28da1ff04411' # Input your api_hash here

token = '808783132:AAHi9saPebiAtDpXKJyKG7k8jHCWzvjRWjU'

admin = [577180091]

# Starting the bot action
bot = telebot.TeleBot(token=token)

customText = ''

# Setting up database
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("new_credentials.json", scope)

client = gspread.authorize(creds)

unsub = client.open("UserBot Database").get_worksheet(1)
pending = client.open("UserBot Database").get_worksheet(2)
joined = client.open("UserBot Database").get_worksheet(3)

@bot.message_handler(commands=['start'])
def start(msg):
    """This initiates the bot into action"""
    user = msg.from_user

    bot.reply_to(msg, f"Hello {user.username}")
    time.sleep(2)

    question = bot.send_message(user.id, "What do you have to tell the users today? Type it down..")

    bot.register_next_step_handler(question, stepTwo)

def stepTwo(msg):
    """Approving the custom text being sent"""

    global customText
    customText = msg.text

    user = msg.from_user

    markup = types.InlineKeyboardMarkup(row_width=2)
    a = types.InlineKeyboardButton("Accept", callback_data='1')
    b = types.InlineKeyboardButton("Decline", callback_data='2')
    markup.add(a, b)
    bot.send_message(user.id, f"Do you wish to continue? Message >> {customText}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user = call.from_user
    logger.info(call)

    if call.data == "1":
        question = bot.send_message(user.id, "Please send the updated database file here >> ")
        bot.register_next_step_handler(question, receiveFile)

    elif call.data == "2":
        bot.send_message(user.id, "Bad Format!!")

    else:
        bot.send_message(user.id, "Bad Format Entirely!!")


@bot.message_handler(content_types=['document'])
def receiveFile(file):
    """Handles all sent documents and audio files"""

    user = file.from_user
    document = file.document
    # b = loop.create_task(sender.download(msg=file))
    # loop.run_until_complete(b)
    bot.send_message(
        user.id,
        "Your custom message is being sent! Please wait for my confirmation that the messages have been sent successfully"
    )

    file_info = bot.get_file(document.file_id)

    file = bot.download_file(file_info.file_path)
    # requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    col_name = ['First Name', 'Last Name', 'Username', 'Id', 'User Status', 'Group Name']

    raw = str(file).split('\\n')
    rawB = [each.split(',') for each in raw[1:]]
    users = []

    for r in rawB:

        try:
            users.append(r[2])

            try:
                index = int(len(pending.get_all_records()) + 2)
                time.sleep(1)

                pending.insert_row([f'{r[0]}', f'{r[1]}', f'{r[2]}', f'{r[3]}'], index=index)

                a = loop.create_task(sender.send(r[2], customText, user))
                loop.run_until_complete(a)

            except Exception:
                pass

        except IndexError as e:

            pass

    bot.send_message(
        user.id,
        "UserBot sending messages!!!!"
    )


def sendMessage(ids):
    """Sends the custom message to the target users"""

    try:
        with TelegramClient("Client", api_id, api_hash).start() as client:

            [client.send_message(each, f"{customText}    -- Reply STOP to terminate subscription.") for each in ids]

    except Exception as e:

        bot.send_message(admin[0], "Failed Sending Message Request")



@bot.message_handler(func=lambda msg: True)
def joined(msg):
    """Checks each updates and validates the user in the spreadsheet"""
    user = msg.from_user

    # Call pending list
    pend = pending.get_all_records()
    time.sleep(1.5)

    # Check user in pending list
    if str(user.id) in pend[3]:
        bot.send_message(admin[1], 'Got it! Adding new user to joined list....')

        index = int(len(joined.get_all_records()) + 2)
        time.sleep(1)

        joined.insert_row([f'{user.first_name}', f'{user.last_name}', f'{user.username}', f'{user.id}'], index=index)

        position = pend[3].index(str(user.id))
        pending.delete_row(index=position)

        # Add to joined
    else:
        pass


print("Bot running.....")
bot.polling()

while True:
    pass
