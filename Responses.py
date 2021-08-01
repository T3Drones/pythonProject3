from datetime import datetime

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from telegram import update



def sample_reponses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi",):
        return "Hey!"

    if user_message in ("help"):
        return "Ask this bot for any of the following by texting the word: balance, chips, tips"


    if user_message in ("time"):
        now = datetime.now()
        date_time = now.strftime("%d/m/%y, %H:%M:%S")
        return str(date_time)
    return "I dont understand"