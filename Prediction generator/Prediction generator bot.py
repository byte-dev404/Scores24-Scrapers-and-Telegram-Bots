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