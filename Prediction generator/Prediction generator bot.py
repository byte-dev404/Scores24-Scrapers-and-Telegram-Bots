import os
import json
import httpx
import logging
from dotenv import load_dotenv

''' Get the bot token either from the .env file ''' 
load_dotenv()
bot_token = os.getenv("PREDICTION_GENERATOR_BOT_TOKEN")

''' Or simply paste it here '''
# bot_token = "~~Enter~~your~~bot~~token~~here~~" # but never forget to remove it before commiting to github


if not bot_token:
    raise TypeError("Error: bot token is missing\nAdd your bot token right after imports then try again.")

start_msg = "Hi, I'm Scores24 Prediction Generator Bot.\nDo /help to see the full list of commands"
help_msg = "Here's the full list of commands that might help.\n\n/start - To start the conversation with bot\n/help - To see all commands and get help\n/contact - To contact my creator\n/generate_prediction - To generate predictions\n\nIf the above doesn't help, you might wanna contact my creator, for that do /contact"
contact_msg = "Contact my creator Mr. Vishwas Batra,\nHere on LinkedIn: https://www.linkedin.com/in/vishwas-batra/"
unknown_msg = "Sorry, I didn't understand that command, maybe because this command is not defined.\nContact the developer via /contact command, if you want to add new features."