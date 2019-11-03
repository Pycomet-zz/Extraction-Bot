from telethon.sync import TelegramClient, events
from pprint import pprint
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
loop = asyncio.get_event_loop()

# ## Defining the need variables
# api_id = '761526'
# api_hash = '71ec605bc89cc9f7d755d3e3fe5798d1'

# Defining the need variables
api_id = '683428' # Input your api_id here
api_hash = '967b28d111f82b906b6f28da1ff04411' # Input your api_hash here

admin = [577180091]

# Initializing the connection
client = TelegramClient("sdsda", api_id=api_id, api_hash=api_hash)
client.start()

# Setting up database
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("new_credentials.json", scope)

sheet = gspread.authorize(creds)

unsub = sheet.open("UserBot Database").get_worksheet(1)
pend = sheet.open("UserBot Database").get_worksheet(2)

# Add handler for "Unsub" to service
@events.register(events.NewMessage('(?i)Unsub'))
async def unsubscribe(msg):
    """Unsubscribe and add to list"""

    user = await client.get_sender()

    # Import users from pending list
    pending = pend.get_all_records()

    if user.id not in pending[3]:
        # Adding to spreadsheet
        index = int(len(unsub.get_all_records()) + 2)
        time.sleep(1)
        unsub.insert_row([f'{user.first_name}', f'{user.last_name}', f'{user.username}', f'{user.id}'], index=index)

        time.sleep(2)
        await client.send_message(admin[0], f"{user.username} Unsubscribed")
        position = pending[3].index(str(user.id))
        pending.delete_row(index=position)

print("Bot running")
client.add_event_handler(unsubscribe)
client.run_until_disconnected()

while True:
    pass

