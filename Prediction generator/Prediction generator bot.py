import os
import json
import httpx
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

''' Get the bot token either from the .env file ''' 
load_dotenv()
bot_token = os.getenv("PREDICTION_GENERATOR_BOT_TOKEN")

''' Or simply paste it here '''
# bot_token = "~~Enter~~your~~bot~~token~~here~~" # but never forget to remove it before commiting to github

if not bot_token:
    raise TypeError("Error: bot token is missing\nAdd your bot token right after imports then try again.")

# Predefined messages for commands
start_msg = "Hi, I'm Scores24 Prediction Generator Bot.\nDo /help to see the full list of commands"
help_msg = "Here's the full list of commands that might help.\n\n/start - To start the conversation with bot\n/help - To see all commands and get help\n/contact - To contact my creator\n/generate_prediction - To generate predictions\n\nIf the above doesn't help, you might wanna contact my creator, for that do /contact"
contact_msg = "Contact my creator Mr. Vishwas Batra,\nHere on LinkedIn: https://www.linkedin.com/in/vishwas-batra/"
unknown_msg = "Sorry, I didn't understand that command, maybe because this command is not defined.\nContact the developer via /contact command, if you want to add new features."

# All selectable options
mode_options = ["Best", "Custom"]
time_options = ["all", "today", "tomorrow"]
sport_options = ["all", 'soccer', 'ice-hockey', 'basketball', 'tennis', 'futsal', 'mma', 'snooker', 'baseball', 'american-football', 'csgo', 'volleyball', 'rugby', 'handball', 'boxing',]

# Exposed api endpoint
predictions_endpoint = "https://scores24.live/graphql"

# Request cookies
cookies = {
    'testValue': '1',
    'bannerValue': '1',
    'userOddFormat': 'EU',
    'machineTimezone': 'GMT+5:30',
    'cookiesAccepted': '1',
    '_ym_uid': '1766933521295718120',
    '_ym_d': '1767272335',
    '_ga': 'GA1.1.1417545567.1767272355',
    '_ym_uid': '1766933521295718120',
    '_ga_ZPJ1YWQ2Z0': 'GS2.1.s1767272355$o1$g0$t1767272359$j56$l0$h0',
    '_ga_L002PTBYML': 'GS2.1.s1767272355$o1$g0$t1767272359$j56$l0$h0',
    '_subid': '1q2aj1titp74p',
    '_token': 'uuid_1q2aj1titp74p_1q2aj1titp74p6962ff732c39b5.82628598',
    's24-session': 'i4pZhwDbN8xBaukDFOu8XaIJdWJ0WD2w1pdAVgO7',
    'clever-counter-86866': '0-1',
    'adScriptNew': '4',
    'latestWidth': '1707',
}

# Request headers
headers = {
    'x-api-token': 'ufnoof',
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://scores24.live/en/predictions',
    'x-api-timestamp': '1768627106',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'x-user-ip': '112.110.54.156',
    'x-user-cache': 'W2ZO6w9f6OdiBrEL9DMG',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'accept': 'application/graphql-response+json, application/graphql+json, application/json, text/event-stream, multipart/mixed',
    'accept-language': 'en-US,en;q=0.9',
    'x-country': 'in',
    'content-type': 'application/json',
    'x-bot-identifier': 'client',
    'x-ssr-ip': '112.110.54.156',
}

# Request params (Default/Best)
json_data = {
    'operationName': 'PredictionsSports',
    'query': 'query PredictionsSports($sportSlugs: [String!], $langSlug: String!, $orderBy: String, $orderType: String, $leagueSlugs: [String], $timezoneOffset: Int, $day: DayEnum, $votesType: PredictionVotesTypeEnum, $first: Int!, $after: String, $topMatches: Boolean, $marketSlugs: [String]) {\n  SportPrediction(\n    sport_slug: $sportSlugs\n    lang: $langSlug\n    day: $day\n    timezone_offset: $timezoneOffset\n    league_slugs: $leagueSlugs\n    votes_type: $votesType\n    order_type: $orderType\n    order_by: $orderBy\n    first: $first\n    after: $after\n    top_matches: $topMatches\n    market_slugs: $marketSlugs\n  ) {\n    sportKey: sport_key\n    slug\n    name\n    count\n    items {\n      edges {\n        cursor\n        node {\n          ...PredictionsCardFragment\n          __typename\n        }\n        __typename\n      }\n      pageInfo {\n        endCursor\n        hasNextPage\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\nfragment PredictionsCardFragment on CachedPrediction {\n  prediction\n  predictionValue: prediction_value\n  allVotesCount: all_votes_count\n  agreedVotesPercent: agreed_votes_percent\n  match {\n    ...MatchCacheFragment\n    uniqueTournament: unique_tournament {\n      ...LeagueCacheFragment\n      name\n      __typename\n    }\n    country {\n      ...CountryFragment\n      __typename\n    }\n    teams {\n      ...TeamCacheFragment\n      name\n      logo\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\nfragment MatchCacheFragment on Match {\n  slug\n  matchDate: match_date\n  langSlug: lang_slug\n  __typename\n}\nfragment LeagueCacheFragment on League {\n  slug\n  langSlug: lang_slug\n  sportSlug: sport_slug\n  __typename\n}\nfragment CountryFragment on Country {\n  name\n  slug\n  iso\n  __typename\n}\nfragment TeamCacheFragment on Team {\n  slug\n  langSlug: lang_slug\n  name\n  temporarilyQualified: temporarily_qualified\n  __typename\n}',
    'variables': {
        'first': 6,
        'langSlug': 'en',
        'sportSlugs': [
            'soccer', 
            'ice-hockey', 
            'basketball', 
            'tennis', 
            'futsal', 
            'mma', 
            'snooker', 
            'baseball', 
            'american-football', 
            'csgo', 
            'volleyball', 
            'rugby', 
            'handball', 
            'boxing',
            ],
        'timezoneOffset': 330,
    },
}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Basic commnads 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=contact_msg)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=unknown_msg)

def main():
    print("Booting up the bot")
    application = ApplicationBuilder().token(bot_token).build()

    # Handlers


    # Attach handlers to bot


    # Unknow handler must be placed below all other handlers, as it consumes every unhandled command
    

    print("Bot successfully initialized, now listening for inputs...")
    application.run_polling()

if __name__ == "__main__":
    main()