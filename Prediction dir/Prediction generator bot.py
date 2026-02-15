import os
import json
# import httpx
from curl_cffi.requests import AsyncSession
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from telegram.error import TimedOut
from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, filters, MessageHandler

''' Get the bot token either from the .env file ''' 
load_dotenv()
bot_token = os.getenv("PREDICTION_GENERATOR_BOT_TOKEN")

''' Or simply paste it here '''
# bot_token = "~~Enter~~your~~bot~~token~~here~~" # but never forget to remove it before commiting to github

if not bot_token:
    raise TypeError("Error: bot token is missing\nAdd your bot token right after imports then try again.")

# Predefined messages for commands
start_msg = "Hi, I'm Scores24 Prediction Generator Bot.\nDo /help to see the full list of commands"
help_msg = "Here's the full list of commands that might help.\n\n/start - To start the conversation with bot\n/help - To see all commands and get help\n/contact - To contact my creator\n/generate_predictions - To generate predictions\n\nIf the above doesn't help, you might wanna contact my creator, for that do /contact"
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

# Helper funcs to handle channel post and private messages
def get_message_and_chat(update: Update):
    if update.message:
        return update.message, update.message.chat_id
    if update.channel_post:
        return update.channel_post, update.channel_post.chat_id
    return None, None

def get_state(context: ContextTypes.DEFAULT_TYPE, update: Update):
    if update.effective_user:
        return context.user_data
    return context.chat_data

# Helper funcs to build keyboard/buttons
def build_mode_keyboard(selected_mode: Optional[str]):
    keyborad = []
    row = []

    for mode in mode_options:
        label = f"✅ {mode}" if mode == selected_mode else mode
        row.append(InlineKeyboardButton(label, callback_data=f"mode: {mode}"))

        if len(row) == 2:
            keyborad.append(row)
            row = []
    if row:
        keyborad.append(row)

    return InlineKeyboardMarkup(keyborad)

def build_time_keyboard(selected_time: Optional[str]):
    keyboard = []
    row = []

    for time_option in time_options:
        label = f"✅ {time_option}" if time_option == selected_time else f"⬜ {time_option}"
        row.append(InlineKeyboardButton(label, callback_data=f"time: {time_option}"))

        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Next ➡️", callback_data="time_next")])
    return InlineKeyboardMarkup(keyboard)

def build_sports_keyboard(selected_sport: Optional[str]):
    keyboard = []
    row = []

    is_all_active = not selected_sport

    for sport in sport_options:
        if sport == "all":
            label = f"✅ All" if is_all_active else "⬜ All"
        else:
            label = f"✅ {sport.title()}" if sport in selected_sport else f"⬜ {sport.title()}"

        row.append(InlineKeyboardButton(label, callback_data=f"sport:{sport}"))

        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Next ➡️", callback_data="sport_next")])
    return InlineKeyboardMarkup(keyboard)

# Helper funcs to extract/format useful data from the json blob
def format_prediction(pred):
    if isinstance(pred, list) and len(pred) == 2:
        market, value = pred
        value = value.replace("_", ".") if isinstance(value, str) else value

        market_map = {
            "handicap1": "Handicap Home",
            "handicap2": "Handicap Away",
            "total_t1_over": "Team 1 Over",
            "total_t1_under": "Team 1 Under",
            "total_t2_over": "Team 2 Over",
            "total_t2_under": "Team 2 Under",
            "double_chance": "Double Chance",
            "one_x_two": "Match Result",
            "both_to_score": "Both Teams to Score",
        }

        market_label = market_map.get(market, market.replace("_", " ").title())
        return f"{market_label} {value}"

    if isinstance(pred, str):
        return pred

    return "Unknown prediction"

def extract_predictions(response_json):
    predictions = []

    sport_blocks = response_json.get("data", {}).get("SportPrediction") or []
    if not isinstance(sport_blocks, list): return predictions

    for sport in sport_blocks:
        if not isinstance(sport, dict): continue

        items = sport.get("items") or {}
        edges = items.get("edges") or []

        if not isinstance(edges, list): continue

        for edge in edges:
            if not isinstance(edge, dict): continue

            node = edge.get("node")
            if not isinstance(node, dict): continue

            match = node.get("match") or {}
            if not isinstance(match, dict): continue

            teams = match.get("teams") or []
            if isinstance(teams, list) and teams:
                team_names = " vs ".join(team.get("name", "Unknown") for team in teams if isinstance(team, dict))
            else:
                team_names = "Unknown match"

            raw_prediction = node.get("prediction")
            prediction_text = format_prediction(raw_prediction)
            prediction_value = node.get("predictionValue")
            confidence = node.get("agreedVotesPercent")
            votes = node.get("allVotesCount")

            unique_tournament = match.get("uniqueTournament") or {}
            league = unique_tournament.get("name", "Unknown league")

            country_obj = match.get("country") or {}
            country = country_obj.get("name", "Unknown country")

            match_date = match.get("matchDate")


            if prediction_text is None and prediction_value is None: continue

            predictions.append({
                "sport": sport.get("name", "Unknown sport"),
                "match": team_names,
                "league": league,
                "country": country,
                "prediction": prediction_text,
                "value": prediction_value,
                "confidence": confidence,
                "votes": votes,
                "match_date": match_date,
            })

    return predictions

# Basic commnads 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _, chat_id = get_message_and_chat(update)
    if not chat_id:
        return
    
    await context.bot.send_message(chat_id=chat_id, text=start_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _, chat_id = get_message_and_chat(update)
    if not chat_id:
        return

    await context.bot.send_message(chat_id=chat_id, text=help_msg)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _, chat_id = get_message_and_chat(update)
    if not chat_id:
        return

    await context.bot.send_message(chat_id=chat_id, text=contact_msg)

# Main prediction command
async def generate_prediction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = get_state(context, update)
    state.clear()
    state["mode"] = None
    state["time"] = None

    message, _ = get_message_and_chat(update)
    if not message:
        return

    try:
        await message.reply_text("Choose a mode for generating prediction:", reply_markup=build_mode_keyboard(None))
    except TimedOut:
        pass

# Follow-up queries handlers for custom prediction
async def handle_mode_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, mode = query.data.split(": ")
    state = get_state(context, update)
    state["mode"] = mode

    if mode == "Best":
        await query.message.delete()
        await context.bot.send_message(chat_id=query.message.chat_id, text="Generating best predictions…")
        context.application.create_task(fetch_prediction(query, context))
        return
    
    if not context.user_data.get("mode"):
        await query.answer("Select a prediction mode!", show_alert=True)
        return
    
    context.user_data["time"] = None  
    await query.edit_message_text(text=f"Now select a time:", reply_markup=build_time_keyboard(None))
    return
    
async def handle_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_data = query.data
    state = get_state(context, update)

    if query.data.startswith("time:"):
        _, time_value = query.data.split(": ")
        state["time"] = time_value

        await query.edit_message_reply_markup(reply_markup=build_time_keyboard(time_value))
        return   

    if user_data == "time_next":
        if not context.user_data.get("time"):
            await query.answer("Select a time option!", show_alert=True)
            return
            
        state["sports"] = set()
        sports_keyboard = build_sports_keyboard(state["sports"])

        await query.edit_message_text(text=f"Now select one or more sports:", reply_markup=sports_keyboard)
        return

async def handle_sport_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    state = get_state(context, update)
    selected = state.setdefault("sports", set())

    if query.data == "sport_next":
        await query.message.delete()
        await context.bot.send_message(chat_id=query.message.chat_id, text="Generating bet slips…")
        context.application.create_task(fetch_prediction(query, context))
        return
    
    _, sport = query.data.split(":", 1)
    sport = sport.strip()
    if sport == "all":
        selected.clear()
    else:
        selected.discard("all")
        if sport in selected:
            selected.remove(sport)
        else:
            selected.add(sport)

    await query.edit_message_reply_markup(reply_markup=build_sports_keyboard(selected))

async def fetch_prediction(query, context):
    # run_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S") # Run ID for development only
    user_data = context.chat_data if not query.from_user else context.user_data
    json_data_copy = json.loads(json.dumps(json_data))
    
    if user_data.get("mode") == "Custom":
        vars = json_data_copy["variables"]

        if user_data['time'] != "all":
            vars["day"] = user_data['time']
        if user_data["sports"]:
            vars['sportSlugs'] = list(user_data["sports"])
        
    async with AsyncSession(timeout=30, impersonate="chrome") as session:
    # async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=30, write=10, pool=10)) as client:
        response = await session.post(url=predictions_endpoint, cookies=cookies, headers=headers, json=json_data_copy)
    
    if response.status_code != 200:
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"Scores24 API error, status code: {response.status_code}")
        return

    response_json = response.json()
    predictions = extract_predictions(response_json)

    if not predictions:
        await context.bot.send_message(chat_id=query.message.chat_id, text="No predictions found for the selected filters.")
        return

    for p in predictions:
        prediction_msg = (
            f"⚔️ {p['match']}\n"
            f"🏆 {p['league']} ({p['country']})\n"
            f"📊 Prediction: {p['prediction']} ({p['value']})\n"
            f"📈 Confidence: {p['confidence']}%\n"
            f"👥 Votes: {p['votes']}\n"
            f"🕒 Match time: {p['match_date']}"
        )

        await context.bot.send_message(chat_id=query.message.chat_id, text=prediction_msg)

    user_data.clear()

# Handler for all unknown commands
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        return

    _, chat_id = get_message_and_chat(update)
    if not chat_id:
        return

    await context.bot.send_message(chat_id=chat_id, text=unknown_msg)

# Error handler
async def error_handler(update: Optional[Update], context: ContextTypes.DEFAULT_TYPE):
    logging.exception("Unhandled error", exc_info=context.error)

    if update and update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An internal error occurred. Please try again later.")

def main():
    print("Booting up the bot")
    application = ApplicationBuilder().token(bot_token).build()

    # Filter to allows both private/group messages AND channel posts
    channel_filter = filters.ChatType.CHANNEL | filters.ChatType.GROUPS | filters.ChatType.PRIVATE

    # Handlers
    start_handler = CommandHandler("start", start_command, filters=channel_filter)
    help_handler = CommandHandler("help", help_command, filters=channel_filter)
    contact_handler = CommandHandler("contact", contact_command, filters=channel_filter)
    generate_prediction_handler = CommandHandler("generate_predictions", generate_prediction_command, filters=channel_filter)
    mode_selection_handler = CallbackQueryHandler(handle_mode_selection, pattern="^(mode:)")
    time_selection_handler = CallbackQueryHandler(handle_time_selection, pattern="^(time:|time_next)")
    sport_selection_handler = CallbackQueryHandler(handle_sport_selection, pattern="^(sport:|sport_next)")
    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)

    # Attach handlers to bot
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(contact_handler)
    application.add_handler(generate_prediction_handler)
    application.add_handler(mode_selection_handler)
    application.add_handler(time_selection_handler)
    application.add_handler(sport_selection_handler)
    application.add_error_handler(error_handler)

    # Unknow handler must be placed below all other handlers, as it consumes every unhandled command
    application.add_handler(unknown_handler)

    print("Bot successfully initialized, now listening for inputs...")
    application.run_polling(allowed_updates=Update.ALL_TYPES) # Starts the bot for listening updates/messages

if __name__ == "__main__":
    main()