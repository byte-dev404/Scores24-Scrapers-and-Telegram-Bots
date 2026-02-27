import sys
from scheduler import schedule_jobs,  add_channel_jobs

sys.path.insert(0, "/home/container/.local")

import os
import json
from curl_cffi.requests import AsyncSession
import logging
from typing import Optional
# from dotenv import load_dotenv
from telegram.error import TimedOut
from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, filters, MessageHandler

''' Get the bot token either from the .env file ''' 
# load_dotenv()
# bot_token = os.getenv("PREDICTION_GENERATOR_BOT_TOKEN")

''' Or simply paste it here '''
bot_token = "~~Enter~~your~~bot~~token~~here~~" # but never forget to remove it before commiting to github

if not bot_token:
    raise TypeError("Error: bot token is missing\nAdd your bot token right after imports then try again.")

# Predefined messages for commands
start_msg = "Hi, I'm Scores24 Prediction Generator Bot.\nDo /help to see the full list of commands"
help_msg = "Here's the full list of commands that might help.\n\n/start - To start the conversation with bot\n/help - To see all commands and get help\n/contact - To contact my creator\n/config - To configure automatic predictions posting\n\nIf the above doesn't help, you might wanna contact my creator, for that do /contact"
contact_msg = "Contact my creator Mr. Vishwas Batra,\nHere on LinkedIn: https://www.linkedin.com/in/vishwas-batra/"
unknown_msg = "Sorry, I didn't understand that command, maybe because this command is not defined.\nContact the developer via /contact command, if you want to add new features."

# All selectable options
mode_options = ["Best", "Custom"]
time_options = ["all", "today", "tomorrow"]
sport_options = ["all", 'soccer', 'ice-hockey', 'basketball', 'tennis', 'futsal', 'mma', 'snooker', 'baseball', 'american-football', 'csgo', 'volleyball', 'rugby', 'handball', 'boxing',]

config_file = "config.json"

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
        row.append(InlineKeyboardButton(label, callback_data=f"mode:{mode}"))

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
        row.append(InlineKeyboardButton(label, callback_data=f"time:{time_option}"))

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

def extract_predictions(response_json, min_confi):
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

            confidence = node.get("agreedVotesPercent")
            if confidence is None or not confidence >= min_confi: continue

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

def is_valid_time(value: str) -> bool:
    try:
        hour, minute = value.split(":")
        hour = int(hour)
        minute = int(minute)
        return 0 <= hour <= 23 and 0 <= minute <= 59
    except Exception:
        return False

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

# Main config command
async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    state = context.user_data
    state.clear()

    state.update({
        "mode": None,
        "time": None,
        "sports": set(),
        "min_confidence": None,
        "post_count": None,
        "post_times": [],
        "target_chat_id": None
    })

    await message.reply_text(
        "Let’s configure automatic predictions posting.\n\n"
        "First step: choose how predictions should be generated."
    )

    await message.reply_text(
        "Choose a mode:",
        reply_markup=build_mode_keyboard(None)
    )

# Follow-up queries handlers for custom prediction
async def handle_mode_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, mode = query.data.split(":")
    state = get_state(context, update)
    state["mode"] = mode

    if mode == "Best":
        state["min_confidence"] = None
        await query.edit_message_text(text="Enter minimum confidence to filter results (0–100):")
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

    if user_data.startswith("time:"):
        _, time_value = user_data.split(":")
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
        state["min_confidence"] = None
        await query.edit_message_text(text="Enter minimum confidence to filter results (0–100):")
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

async def handle_numeric_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    state = context.user_data
    text = message.text.strip()

    if state.get("min_confidence") is None:
        if not text.isdigit():
            await message.reply_text("Please enter a number between 0 and 100.")
            return

        value = int(text)
        if not 0 <= value <= 100:
            await message.reply_text("Confidence must be between 0 and 100.")
            return

        state["min_confidence"] = value
        await message.reply_text(
            "Great.\n\n"
            "How many times per day should I post predictions?\n"
            "Example: 1, 2, 3"
        )
        return

    if state.get("post_count") is None:
        if not text.isdigit():
            await message.reply_text("Please enter a valid number.")
            return

        count = int(text)
        if count <= 0 or count > 10:
            await message.reply_text("Post count must be between 1 and 10.")
            return

        state["post_count"] = count
        state["post_times"] = []

        await message.reply_text(
            f"Okay.\n\n"
            f"Send time for post 1 in 24-hour format (HH:MM).\n"
            f"Example: 09:30"
        )
        return

    if len(state["post_times"]) < state["post_count"]:
        if not is_valid_time(text):
            await message.reply_text(
                "Invalid time format.\n"
                "Please use HH:MM in 24-hour format."
            )
            return

        state["post_times"].append(text)

        index = len(state["post_times"])
        total = state["post_count"]

        if index < total:
            await message.reply_text(
                f"Time {index} saved.\n\n"
                f"Send time for post {index + 1} (HH:MM)."
            )
            return

        await message.reply_text(
            "All post times saved.\n\n"
            "Now send the target channel ID where I should post predictions.\n"
            "Tip: paste the numeric channel ID."
        )
        return

    if state.get("target_chat_id") is None:
        try:
            target_chat_id = int(text)
        except ValueError:
            await message.reply_text("Please send a valid numeric channel ID.")
            return

        state["target_chat_id"] = target_chat_id

        config = {
            "enabled": True,
            "mode": state["mode"],
            "time_filter": state["time"],
            "sports": list(state["sports"]),
            "min_confidence": state["min_confidence"],
            "post_times": state["post_times"]
        }

        try:
            save_config(target_chat_id, config)
            add_channel_jobs(context.bot, target_chat_id, config)
        except Exception:
            await message.reply_text(
                "Failed to save configuration. Please try again."
            )
            return

        await message.reply_text(
            "Configuration saved successfully.\n\n"
            "I will now post predictions automatically at the scheduled times."
        )

        state.clear()

def save_config(target_chat_id: int, config: dict):
    try:
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        data[str(target_chat_id)] = config

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        logging.exception("Failed to save config")
        raise e

async def fetch_predictions_core(config: dict):
    json_data_copy = json.loads(json.dumps(json_data))

    if config.get("mode") == "Custom":
        vars = json_data_copy["variables"]

        if config.get("time_filter") != "all":
            vars["day"] = config.get("time_filter")

        if config.get("sports"):
            vars["sportSlugs"] = config.get("sports")

    async with AsyncSession(timeout=30, impersonate="chrome") as session:
        response = await session.post(url=predictions_endpoint, cookies=cookies, headers=headers, json=json_data_copy)

    if response.status_code != 200:
        raise RuntimeError(f"Scores24 API error: {response.status_code}")

    response_json = response.json()
    return extract_predictions(response_json, config["min_confidence"])

async def fetch_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = get_state(context, update)
    _, chat_id = get_message_and_chat(update)

    config = {
        "mode": user_data.get("mode"),
        "time_filter": user_data.get("time"),
        "sports": list(user_data.get("sports", [])),
        "min_confidence": user_data.get("min_confidence"),
    }

    try:
        predictions = await fetch_predictions_core(config)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=str(e))
        return

    if not predictions:
        await context.bot.send_message(chat_id=chat_id, text="No predictions found for the selected filters.")
        return

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

# Returns built bot to run it from a centralized file instead of calling it here
def build_app():
    application = ApplicationBuilder().token(bot_token).build()

    private_chat = filters.ChatType.PRIVATE

    application.add_handler(CommandHandler("start", start_command, filters=private_chat))
    application.add_handler(CommandHandler("help", help_command, filters=private_chat))
    application.add_handler(CommandHandler("contact", contact_command, filters=private_chat))
    application.add_handler(CommandHandler("config", config_command, filters=private_chat))

    application.add_handler(CallbackQueryHandler(handle_mode_selection, pattern="^(mode:)"))
    application.add_handler(CallbackQueryHandler(handle_time_selection, pattern="^(time:|time_next)"))
    application.add_handler(CallbackQueryHandler(handle_sport_selection, pattern="^(sport:|sport_next)"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numeric_input))

    application.add_error_handler(error_handler)
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    async def post_init(app):
        schedule_jobs(app.bot)

    application.post_init = post_init

    return application

def main():
    print("Booting up the bot")

    application = build_app()

    async def post_init(app):
        schedule_jobs(app.bot)

    application.post_init = post_init

    print("Bot successfully initialized, now listening for inputs...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()