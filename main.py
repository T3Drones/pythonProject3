import threading
import time

import Constants as keys
from telegram.ext import *
import Responses as R
import logging
from telegram import Update
from telegram.ext import (Updater, CommandHandler, CallbackContext)



import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()


print("Bot Started")
def start_command(update: Update, _: CallbackContext) -> None:
    """Start user by sending chat_id and name"""
    _.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_user.name))
    _.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_chat.id))
    _.bot.send_message(chat_id=1600750501, text=str(update.effective_chat.id) + '\n' + str(update.effective_user.full_name))
    update.message.reply_text(
        ''
        'Welcome, Please save the number above, '
        
        'text help for a list of commands'
    )

def help_command(update, context):
    update.message.reply_text("Help Response")

def users_command(update, context):
    user = db.collection('messages').document('message').get()

    textmessage = user.to_dict()
    update.message.reply_text(textmessage)

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_reponses(text)

    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):

    for doc in doc_snapshot:
        message = doc.get('text')
        if len(message) > 1:
            print(f'Received document snapshot: {message}')
            db.collection('messages').document('message').update(
                {

                    'text': "",
                    'telegram': "",


                }
            )






    callback_done.set()

doc_ref = db.collection(u'messages').document(u'message')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)









def main():
    updater =Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("users", users_command))
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    db.collection('messages').document('message')

    updater.start_polling(4)
    updater.idle()

main()


