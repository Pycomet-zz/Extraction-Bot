############################################################################################################################################################################
############################################################################################################################################################################

## This code was written by Codefred
## Compactible with Python3 Interpreter

############################################################################################################################################################################
############################################################################################################################################################################

## This script extracts users information from Telegram Groups
## And updates the extracts into a Google Spreadsheet for Admin Access

# https://dry-scrubland-17857.herokuapp.com/ | https://git.heroku.com/dry-scrubland-17857.git  ## Heroku Access

############################################################################################################################################################################

# Importing necessary libraries
import pandas
import telebot
from telebot import types
from telethon import TelegramClient, events
from pprint import pprint
import logging
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv


## Setup Logging
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="extract.log", format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


## Defining the need variables
api_id = '683428' # Input your api_id here
api_hash = '967b28d111f82b906b6f28da1ff04411' # Input your api_hash here


token = '808783132:AAHi9saPebiAtDpXKJyKG7k8jHCWzvjRWjU'

admin = [577180091]

## Connection of all the integrated APIs
bot = TelegramClient("sdsda", api_id, api_hash).start(bot_token=token) # Starting Telegram Bot API

## Setting up database
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("new_credentials.json", scope)

client = gspread.authorize(creds)

# sheet1 = client.open("Users Database").sheet1
sheet2 = client.open("UserBot Database").sheet1

lastExtract = 'No Extracted Information!!'

fieldnames = ['First Name', 'Last Name', 'Username', 'Id', 'User Status', 'Group Name']

############################################################################################################################################################################
############################################################################################################################################################################

idDatabase = [] # Storing channel IDs in an Array


############################################################################################################################################################################
############################################################################################################################################################################

###  HANDLING ACTIONS WITH BOT

############################################################################################################################################################################
############################################################################################################################################################################


@bot.on(events.NewMessage(pattern='/extract'))
async def handleExtraction(msg):
    """Decision Handler For Admin To Update Database"""

    user = await msg.get_sender()
    await msg.reply(f"Hello  Sir {user.username}")


    if user.id not in admin:

        await msg.reply("Sorry, you are not authorized to interact with me!") # Replying users which are not admins

    else:
        
        await bot.send_message(user.id, lastExtract)

        await bot.send_message(user.id, "Google Sheet Database Updating......")

        # Read Group Id from Database
        database = sheet2.get_all_records()
        lenOfDatabase = len(database)

        links = [database[each]['GROUP ID'] for each in range(lenOfDatabase)]
        
        [await getMembers(user, link, msg) for link in links] # Iterating through the update process

        await bot.send_message(user.id, "Database Updated!!", file="Users.csv")


async def getMembers(user, link, msg):
    """Getting Channel Members"""

    # Opening the file
    file = open("Users.csv", "w", encoding="utf8")
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Adding lastExtract to update admin on last extracts made
    global lastExtract
    runTime = time.asctime()
    lastExtract = f"Your last extraction was on {runTime}"

    channel = await bot.get_entity(link)
    members = await bot.get_participants(channel) # Return all users and their information

    numberOfMembers = len(members)

    groupName = link.split("/")[1]

    await bot.send_message(user.id, f"Updating {numberOfMembers} Members In {groupName.upper()} To Database Started!!")

    # await sendMembersToDb(user.id, members) # Move To Next Step
    writeToFile(members, groupName) # Move To Next Step

    await bot.send_message(user.id, f"Updating Users From The Next Group Loading....")

    return lastExtract

# async def sendMembersToDb(userid, members):
#     """Send Updates to User Google Sheet Database"""
#
#     database = sheet1.get_all_values()
#
#     ids = [data[3] for data in database]
#     time.sleep(1)
#
#     for user in members:
#
#         if user.bot == False:
#
#             if str(user.id) not in ids:
#
#                 await bot.send_message(userid, f"Added member {members.index(user)} of  to the database")
#                 index = int(len(sheet1.get_all_records()) + 2)
#                 time.sleep(1)
#
#                 if str(user.status) == "UserStatusRecently()":
#                     status = "Last Seen Not Long Ago"
#                 elif str(user.status) == "UserStatusLastWeek()":
#                     status = "Last Seen Last Week"
#                 elif str(user.status) == "UserStatusLastMonth()":
#                     status = "Last Seen Last Month"
#                 else:
#                     status = "User Has Not Been Active"
#
#                 sheet1.insert_row([f'{user.first_name}', f'{user.last_name}', f'@{user.username}', f'{user.id}', f'{status}'], index=index)
#
#                 time.sleep(1)

def writeToFile(members, groupName):
    """Writes the Users into an xls file"""
    #Open csv file
    with open("Users.csv", "a", encoding="utf8") as file:

    #Input headers
        writer = csv.DictWriter(file, fieldnames=fieldnames)
    #Input scraped content
        for user in members:
            if user.bot == False:

                if str(user.status) == "UserStatusRecently()":
                    status = "Last Seen Not Long Ago"
                elif str(user.status) == "UserStatusLastWeek()":
                    status = "Last Seen Last Week"
                elif str(user.status) == "UserStatusLastMonth()":
                    status = "Last Seen Last Month"
                else:
                    status = "User Has Not Been Active"

                writer.writerow({
                    'First Name': user.first_name,
                    'Last Name': user.last_name,
                    'Username': user.username,
                    'Id': int(user.id),
                    'User Status': status,
                    'Group Name': str(groupName)
                })


############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################

# customText = ''
#
# @bot.on(events.NewMessage(pattern='/start'))
# async def start(msg):
#     """This initiates the bot into action"""
#     user = await msg.get_sender()
#
#     await bot.send_message(user.id, f"Hello {user.username}")
#     time.sleep(2)
#
#     question = bot.send_message(user.id, "What do you have to tell the users today? Type it down..")
#
#     bot2 = telebot.TeleBot(token=token).polling()
#     bot2.register_next_step_handler(question, stepTwo)
#
# async def stepTwo(msg):
#     """Approving the custom text being sent"""
#
#     global customText
#     customText = msg.text
#
#     user = await msg.get_sender()
#
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     a = types.InlineKeyboardButton("Accept", callback_data='1')
#     b = types.InlineKeyboardButton("Decline", callback_data='2')
#     markup.add(a, b)
#     await bot.send_message(user.id, f"Do you wish to continue? Message >> {customText}", reply_markup=markup)
#
# @bot.on(events.CallbackQuery(func=lambda call: True))
# async def callback(call):
#
#     user = await call.get_sender()
#
#     logger.info(call)
#
#     if call.data == "1":
#         question = bot.send_message(user.id, "Please send the updated database file here >> ")
#         # await bot.register_next_step_handler(question, receiveFile)
#         await bot.send_message(
#             user.id,
#             "Your custom message is being sent! Please wait for my confirmation that the messages have been sent successfully"
#         )
#
#         col_name = ['First Name', 'Last Name', 'Username', 'Id', 'User Status', 'Group Name']
#         data = pandas.read_csv('Users.csv', names=col_name)
#
#         ids = data.Id.tolist()
#         pprint(ids)
#
#         await sendMessage(ids)
#
#     elif call.data == "2":
#         await bot.send_message(user.id, "Bad Format!!")
#
#     else:
#         await bot.send_message(user.id, "Bad Format Entirely!!")
#
# # @bot.on(events.NewMessage(pattern=['document']))
# # async def receiveFile(file):
# #     """Handles all sent documents and audio files"""
# #
# #     user = await file.get_sender()
# #
# #     await bot.send_message(
# #         user.id,
# #         "Your custom message is being sent! Please wait for my confirmation that the messages have been sent successfully"
# #     )
# #
# #     col_name = ['First Name', 'Last Name', 'Username', 'User Id', 'User Status', 'Group Name']
# #     data = pandas.read_csv(file, names=col_name)
# #
# #     ids = data.UserId.tolist()
# #     pprint(ids)
# #
# #     await sendMessage(ids)
#
# async def sendMessage(ids):
#     """Sends the custom message to the target users"""
#
#     try:
#         with TelegramClient("Client", api_id=api_id, api_hash=api_hash).start() as client:
#
#             [client.send_message(each, f"{customText}    -- Reply STOP to terminate subscription.") for each in ids]
#
#

############################################################################################################################################################################
############################################################################################################################################################################

# Polling Bot
print("Bot running.....")

bot.run_until_disconnected()

while True:
    pass

    
    


############################################################################################################################################################################
############################################################################################################################################################################