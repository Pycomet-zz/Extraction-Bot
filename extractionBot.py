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
import telebot
from telebot import types
from telethon import TelegramClient, events
from pprint import pprint
import logging
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random import randint as rand
import csv
from flask import Flask, request
import os


## Setup Logging 
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="extract.log", format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


## Defining the need variables
api_id = '683428' # Input your api_id here
api_hash = '967b28d111f82b906b6f28da1ff04411' # Input your api_hash here


token = '927041875:AAHr9CfWRwJhXMArxIwwyjLL12es8DI62VI'

admin = [577180091]

## Connection of all the integrated APIs
bot = TelegramClient("Tebsfa", api_id, api_hash).start(bot_token=token) # Starting Telegram Bot API 

server = Flask(__name__)

## Setting up database
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

sheet1 = client.open("Users Database").sheet1
sheet2 = client.open("Group Database").sheet1

lastExtract = 'No Extracted Information!!'

############################################################################################################################################################################
############################################################################################################################################################################

idDatabase = [] # Storing channel IDs in an Array


############################################################################################################################################################################
############################################################################################################################################################################

###  HANDLING ACTIONS WITH BOT

############################################################################################################################################################################
############################################################################################################################################################################


@bot.on(events.NewMessage(pattern='/start'))
async def handleExtraction(msg):
    """Decison Handler For Admin To Update Database"""

    user = await msg.get_sender()
    await msg.reply(f"Hello {user.username}")

    if user.id not in admin:

        await msg.reply("Sorry, you are not authorized to interact with me!") # Replying users which are not admins

    else:
        
        await bot.send_message(user.id, lastExtract)

        await bot.send_message(user.id, "Google Sheet Database Updating......")

        # Read Group Id from Database
        database = sheet2.get_all_records()
        lenOfDatabase = len(database)

        links = [database[each]['GROUP ID'] for each in range(lenOfDatabase)]
        
        [await getMembers(user, link) for link in links] # Iterating through the update process

        await bot.send_message(user.id, "Database Updated!!")


############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################



async def getMembers(user, link):
    """Getting Channel Members"""

    # Adding lastExtract to update admin on last extracts made
    global lastExtract
    runTime = time.asctime()
    lastExtract = f"Your last extraction was on {runTime}"

    channel = await bot.get_entity(link)

    members = await bot.get_participants(channel) # Return all users and their information

    numberOfMembers = len(members)

    await bot.send_message(user.id, f"Updating Database with {numberOfMembers} Members")

    await sendMembersToDb(user.id, members) # Move To Next Step
    # writeToFile(members, filename) # Move To Next Step

    return lastExtract

############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################


async def sendMembersToDb(userid, members):
    """Send Updates to User Google Sheet Database"""

    database = sheet1.get_all_values()

    ids = [data[3] for data in database]
    time.sleep(1)
    
    for user in members:
        logger.debug
        if user.bot == False:
            
            if str(user.id) not in ids:

                await bot.send_message(userid, f"Added {members.index(user)} member to the database")
                index = int(len(sheet1.get_all_records()) + 2)
                time.sleep(1)

                if str(user.status) == "UserStatusRecently()":
                    status = "Last Seen Not Long Ago"
                elif str(user.status) == "UserStatusLastWeek()":
                    status = "Last Seen Last Week"
                elif str(user.status) == "UserStatusLastMonth()":
                    status = "Last Seen Last Month"
                else:
                    status = "User Has Not Been Active"

                sheet1.insert_row([f'{user.first_name}', f'{user.last_name}', f'@{user.username}', f'{user.id}', f'{status}'], index=index)

                time.sleep(1)


def writeToFile(members, filename):
    """Writes the Users into an xls file"""

    #Open csv file
    with open(f"{filename}_Users.xlsx", "w", newline='') as file:

    #Input headers
        fieldnames = ['First Name', 'Last Name', 'Username', 'User Id', 'User Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

    #Input scraped content
        for user in members:
            if user.bot == False:
                writer.writerow({
                    'First Name': user.first_name,
                    'Last Name': user.last_name,
                    'Username': user.username,
                    'User Id': user.id,
                    'User Status': user.status
                })
    quit()


############################################################################################################################################################################


    # Polling Bot
print("Bot running.....")
    # bot.polling(none_stop=True)
bot.run_until_disconnected()

while True:
    pass


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dry-scrubland-17857.herokuapp.com/' + token)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


    


    
    


############################################################################################################################################################################
############################################################################################################################################################################