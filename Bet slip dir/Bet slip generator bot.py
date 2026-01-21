import os
import json
import httpx
import logging 
from timezonefinder import TimezoneFinder
from typing import Optional
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from dotenv import load_dotenv 
from telegram.error import TimedOut
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

'''Load your token form .env'''
# load_dotenv()
# bot_token = os.getenv("BET_SLIP_GENERATOR_BOT_TOKEN") 

'''Or paste it here but never forget to remove it before commiting to github'''
# bot_token = "~~Enter~~your~~bot~~token~~here~~" 

start_msg = "Hi, I'm Scores24 Bet Slip Generator Bot.\nDo /help to see the full list of commands"
help_msg = "Here's the full list of commands that might help.\n\n/start - To start the conversation with bot\n/help - To see all commands and get help\n/contact - To contact my creator\n/generate_bet_slip - To generate bet slip\n\nIf the above doesn't help, you might wanna contact my creator, for that do /contact"
contact_msg = "Contact my creator Mr. Vishwas Batra,\nHere on LinkedIn: https://www.linkedin.com/in/vishwas-batra/"
unknown_msg = "Sorry, I didn't understand that command, maybe because this command is not defined.\nContact the developer via /contact command, if you want to add new features."

sports = ['all', 'soccer', 'basketball', 'tennis', 'ice-hockey', 'table-tennis', 'volleyball', 'handball', 'baseball', 'american-football', 'rugby', 'cricket', 'mma', 'boxing', 'snooker', 'futsal', 'waterpolo', 'badminton', 'darts', 'csgo', 'dota2', 'lol', 'horse-racing']
time_options = ['2 hours', '6 hours', '12 hours', '24 hours', '48 hours']
market_options = ['All', 'Match Result', 'Double Chance', 'Over/Under', 'Correct Score', 'Both Teams to Score', 'Handicap', 'Corners', 'Fouls', 'Cards', 'Shots', 'Off-sides']
market_translation = {
    'All': 'all',
    'Match Result': 'results',
    'Double Chance': 'doublechance',
    'Over/Under': 'totals',
    'Correct Score': 'correctscore',
    'Both Teams to Score': 'btts',
    'Handicap': 'handicaps',
    'Corners': 'corners',
    'Fouls': 'fouls',
    'Cards': 'cards',
    'Shots': 'shots',
    'Off-sides': 'offsides',
}
market_translation_for_display = {v: k for k, v in market_translation.items()}
step_odd_from = "odd_from"
step_odd_to = "odd_to"
step_events = "events"

cookies = {
    'testValue': '1',
    'bannerValue': '1',
    'userOddFormat': 'EU',
    'machineTimezone': 'GMT+5:30',
    's24-session': 'npy5pGeYrwdqx2ggFVVSKlwg9c5XirxHTmZJQzXz',
    'cookiesAccepted': '1',
    '_ym_uid': '1766933521295718120',
    '_ym_d': '1767272335',
    '_ym_isad': '2',
    '_ga': 'GA1.1.1417545567.1767272355',
    '_ym_uid': '1766933521295718120',
    '_ga_ZPJ1YWQ2Z0': 'GS2.1.s1767272355$o1$g0$t1767272359$j56$l0$h0',
    '_ga_L002PTBYML': 'GS2.1.s1767272355$o1$g0$t1767272359$j56$l0$h0',
    'promo-proxy-9d962': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1wic3RyZWFtc1wiOntcIjE0MzBcIjoxNzY3MjUyNDM0LFwiMTQzNFwiOjE3NjcyNzIzMjQsXCIxNDMyXCI6MTc2NzI3MjM2MixcIjY0MjNcIjoxNzY3MjcyNDk1LFwiMTQzMVwiOjE3NjcyNzI4MzR9LFwiY2FtcGFpZ25zXCI6e1wiMTBcIjoxNzY3MjUyNDM0fSxcInRpbWVcIjoxNzY3MjUyNDM0fSJ9.PmGw5A_sjk8pmSsQbcWmFQolPn4kuSWoG63BnNy-AAE',
    'clever-counter-86866': '0-1',
    'promo-proxy-_subid': '2euq92mhpcnfr',
    'promo-proxy-_token': 'uuid_2euq92mhpcnfr_2euq92mhpcnfr69567dbe5a7d78.52230640',
    'adScriptNew': '1',
}

headers = {
    'accept': 'application/graphql-response+json, application/graphql+json, application/json, text/event-stream, multipart/mixed',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://scores24.live',
    'priority': 'u=1, i',
    'referer': 'https://scores24.live/en/accumulators/builder',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-api-timestamp': '1767274054',
    'x-api-token': 'tolxho',
    'x-bot-identifier': 'client',
    'x-country': 'in',
    'x-ssr-ip': '2402:8100:2235:e969:b4e8:d120:3753:556a',
    'x-user-cache': 'W2ZO6w9f6OdiBrEL9DMG',
    'x-user-ip': '2402:8100:2235:e969:b4e8:d120:3753:556a',
}

payload = { # Actual working payload with default values
    'operationName': 'CustomAccumFeed',
    'query': 'query CustomAccumFeed($sportSlugs: [String], $leagueSlugs: [String], $hours: Int, $events: Int, $markets: [String], $oddFrom: Float, $oddTo: Float, $langSlug: String!, $couponKey: String, $excludeIds: [String], $audience: String!) {\n  CustomExpress(\n    sport_slugs: $sportSlugs\n    leagues: $leagueSlugs\n    hours: $hours\n    events: $events\n    markets: $markets\n    odd_from: $oddFrom\n    odd_to: $oddTo\n    lang: $langSlug\n    couponKey: $couponKey\n    exclude_ids: $excludeIds\n    audience: $audience\n  ) {\n    ...AccumFragment\n    resetIds: reset_ids\n    trends {\n      ...AccumTrendFragment\n      __typename\n    }\n    bookmakers {\n      ...AccumBookmakerFragment\n      __typename\n    }\n    legalBookmakers: legal_bookmakers {\n      langSlug: lang_slug\n      name\n      slug\n      logo\n      color\n      favicon\n      bonus\n      bonusCurrency: bonus_currency\n      hasPromotions: has_promotions\n      bonusTypeName: bonus_type_name\n      __typename\n    }\n    __typename\n  }\n}\nfragment AccumFragment on ExpressCoupon {\n  langSlug: lang_slug\n  section\n  couponKey: coupon_key\n  sportSlug: sport_slug\n  marketCategory: market_category\n  hasLegal: has_legal\n  probability\n  rate\n  __typename\n}\nfragment AccumTrendFragment on ExpressTrend {\n  id\n  groupedFacts: grouped_facts {\n    title\n    facts {\n      fact\n      text\n      team {\n        ...TeamCacheFragment\n        logo\n        __typename\n      }\n      referee {\n        ...RefereeCacheFragment\n        logo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  factsCount: facts_count\n  length\n  priority\n  rate\n  market {\n    category\n    type\n    subtype\n    __typename\n  }\n  match {\n    ...MatchCacheFragment\n    type\n    leagueSlug: league_slug\n    sportSlug: sport_slug\n    uniqueTournamentName: unique_tournament_name\n    tournament: unique_tournament {\n      ...LeagueCacheFragment\n      name\n      __typename\n    }\n    teams {\n      ...TeamCacheFragment\n      logo\n      name\n      country {\n        iso\n        __typename\n      }\n      __typename\n    }\n    country {\n      ...CountryFragment\n      __typename\n    }\n    __typename\n  }\n  bookmakerSlug: bookmaker_slug\n  odds {\n    bookmakerSlug: bookmaker_slug\n    odd\n    __typename\n  }\n  __typename\n}\nfragment TeamCacheFragment on Team {\n  slug\n  langSlug: lang_slug\n  name\n  temporarilyQualified: temporarily_qualified\n  __typename\n}\nfragment RefereeCacheFragment on Referee {\n  slug\n  name\n  langSlug: lang\n  __typename\n}\nfragment MatchCacheFragment on Match {\n  slug\n  matchDate: match_date\n  langSlug: lang_slug\n  __typename\n}\nfragment LeagueCacheFragment on League {\n  slug\n  langSlug: lang_slug\n  sportSlug: sport_slug\n  __typename\n}\nfragment CountryFragment on Country {\n  name\n  slug\n  iso\n  __typename\n}\nfragment AccumBookmakerFragment on ExpressBookmaker {\n  bookmaker {\n    langSlug: lang_slug\n    name\n    slug\n    logo\n    color\n    favicon\n    bonus\n    bonusCurrency: bonus_currency\n    hasPromotions: has_promotions\n    bonusTypeName: bonus_type_name\n    __typename\n  }\n  slug\n  rate\n  probability\n  __typename\n}',
    'variables': {
        'audience': 'us',
        'couponKey': 'custom',
        'events': 15,
        'excludeIds': [],
        'hours': 48,
        'langSlug': 'en',
        'leagueSlugs': [],
        'markets': ['all'],
        'oddFrom': 1.1,
        'oddTo': 3.0,
        'sportSlugs': [],
    },
}

tf = TimezoneFinder()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

def request_location_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Share location", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def build_sports_keyboard(selected: set):
    keyboard = []
    row = []

    is_all_active = not selected

    for sport in sports:
        if sport == "all":
            label = f"✅ All" if is_all_active else "All"
        else:
            label = f"✅ {sport.title()}" if sport in selected else sport.title()

        row.append(InlineKeyboardButton(label, callback_data=f"sport:{sport}"))

        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Next ➡️", callback_data="sport_next")])
    return InlineKeyboardMarkup(keyboard)

def build_time_range_keyboard(selected: Optional[str]):
    keyboard = []
    row = []

    for time_option in time_options:
        label = f"✅ {time_option}" if time_option == selected else f"🔳 {time_option}"
        row.append(InlineKeyboardButton(label, callback_data=f"time_range:{time_option}"))

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Next ➡️", callback_data="time_next")])
    return InlineKeyboardMarkup(keyboard)

def build_market_keyboard(selected: Optional[str]):
    keyboard = []
    row = []

    for market in market_options:
        label = f"✅ {market}" if market == selected else f"🔳 {market}"
        row.append(InlineKeyboardButton(label, callback_data=f"market:{market}"))

        if len(row) == 2:
            keyboard.append(row)
            row = []
            
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("Next ➡️", callback_data="market_next")])
    return InlineKeyboardMarkup(keyboard)

def pick_best_odd(odds):
    return min(o["odd"] for o in odds)

def extract_trend_text(trend, limit=2):
    lines = []
    for group in trend.get("groupedFacts", []):
        for fact in group.get("facts", []):
            if fact.get("text"):
                lines.append(fact["text"])
            if len(lines) == limit:
                return lines
    return lines

def format_trend_card(trend, user_tz: str):
    match = trend["match"]
    market = trend["market"]

    home = match["teams"][0]["name"]
    away = match["teams"][1]["name"]

    dt_utc = datetime.strptime(match["matchDate"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    try: tz = ZoneInfo(user_tz)
    except Exception: tz = timezone.utc
    dt_local = dt_utc.astimezone(tz)
    date_str = dt_local.strftime("%a, %b %d")
    time_str = dt_local.strftime("%I:%M %p")
    offset = dt_local.utcoffset()
    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    total_minutes = abs(total_minutes)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    gmt_label = f"GMT {sign}{hours:02d}:{minutes:02d}"

    sport = match["sportSlug"].replace("-", " ").title()
    league = match["tournament"]["name"]

    market_name = market_translation_for_display.get(market["category"], market["category"].replace("-", " ").title())

    if "over" in market["type"] or "under" in market["type"]:
        tip = f'{market["type"][6:].capitalize()} {market["subtype"].replace("_", ".")}'
    else:
        tip = market["subtype"].upper()

    odd = pick_best_odd(trend["odds"])
    trend_lines = extract_trend_text(trend, limit=2)
    trend_text = "\n".join(trend_lines)
    
    streak_count = len(trend_lines)
    base = int(trend.get("rate", 0) * 100)

    confidence = base + (streak_count * 10)
    confidence = max(40 if streak_count else 20, min(confidence, 95))

    sport_emoji = {"soccer": "⚽", "basketball": "🏀", "tennis": "🎾", "ice-hockey": "🏒", "table-tennis": "🏓", "volleyball": "🏐", "baseball": "⚾", "american-football": "🏈", "rugby": "🏉", "cricket": "🏏", "mma": "🥋", "boxing": "🥊", "snooker": "🎱", "waterpolo": "🤽", "badminton": "🏸", "darts": "🎯", "horse-racing": "🏇"}.get(match["sportSlug"], "🎮")

    message = (
        f"{sport_emoji} {sport}\n"
        f"⚔️ {home} vs {away}\n"
        f"🕛 {time_str} on {date_str} {gmt_label}\n"
        f"🏆 {league}\n"
        f"📊 {market_name}\n"
        f"🎯 {tip}\n"
        f"💰 Odds: {odd:.2f}\n"
        f"📈 Confidence: {confidence}%\n"
    )

    if trend_text:
        message += f"\n{trend_text}\n"

    return message

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "timezone" not in context.user_data:
        await update.message.reply_text(
            "To show match times correctly, please share your location.",
            reply_markup=request_location_keyboard()
        )
        return

    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_msg)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat, lon = location.latitude, location.longitude

    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        tz_name = "UTC"

    context.user_data["timezone"] = tz_name

    await update.message.reply_text(
        f"✅ Location saved.\nTimezone set to {tz_name}.\nYou can now use /generate_bet_slip.",
        reply_markup=ReplyKeyboardRemove()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=contact_msg)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=unknown_msg)

async def generate_bet_slip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sports"] = set()
    context.user_data["time_range"] = None
    reply_markup = build_sports_keyboard(context.user_data["sports"])

    try: 
        await update.message.reply_text("Select one or more sports, then press Next:", reply_markup=reply_markup)
    except TimedOut:
        pass

async def handle_sport_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    selected = context.user_data.setdefault("sports", set())

    if data == "sport_next":
        if not selected:
            pass

        context.user_data["time_range"] = None

        await query.edit_message_text(text=f"Now select a time range:", reply_markup=build_time_range_keyboard(None))
        return
    
    _, sport = data.split(":")
    if sport == "all":
        selected.clear()
    else:
        selected.discard("all")
        if sport in selected:
            selected.remove(sport)
        else:
            selected.add(sport)

    await query.edit_message_reply_markup(reply_markup=build_sports_keyboard(selected))

async def handle_time_range_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    
    if data == "time_next":
        selected_time_range = context.user_data.get("time_range")
        if not selected_time_range:
            await query.answer("Select a time option...!", show_alert=True)
            return
            
        context.user_data["market"] = None
        await query.edit_message_text(text=f"Now select a market:", reply_markup=build_market_keyboard(None))
        return

    _, event = data.split(":", 1)
    context.user_data["time_range"] = event
    await query.edit_message_reply_markup(reply_markup=build_time_range_keyboard(event))

async def handle_market_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "market_next":
        selected_market = context.user_data.get("market")
        if not selected_market:
            await query.answer("Select a market", show_alert=True)
            return
        
        translated = market_translation[selected_market]
        context.user_data["market_converted"] = translated
        context.user_data["step"] = step_odd_from

        await query.edit_message_text(text=f"Enter minimum odd between (1.1 to 2.9):")
        return
    
    _, market = data.split(":", 1)
    context.user_data["market"] = market

    await query.edit_message_reply_markup(reply_markup=build_market_keyboard(market))

async def handle_numeric_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step")
    if not step:
        return
    
    text = update.message.text.strip()

    if step in (step_odd_from, step_odd_to):
        try:
            value = float(text)
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")
            return

    if step == step_odd_from:
        if not 1.1 <= value <= 2.9:
            await update.message.reply_text("Minimum odd must be between 1.1 and 2.9.")
            return
        
    if step == step_odd_to:
        if not 1.2 <= value <= 3.0:
            await update.message.reply_text("Maximum odd must be between 1.2 and 3.0.")
            return
        
    if step == step_odd_from:
        context.user_data["odd_from"] = value
        context.user_data["step"] = step_odd_to
        await update.message.reply_text("Enter maximum odd:")
        return
    
    if step == step_odd_to:
        if value < context.user_data["odd_from"]:
            await update.message.reply_text("Maximum odd must be greater than minimum odd.")
            return
        
        context.user_data["odd_to"] = value
        context.user_data["step"] = step_events
        await update.message.reply_text("Enter maximum number of events between (1 to 15):")
        return

    if step == step_events:
        if not text.isdigit():
            await update.message.reply_text("Events must be a whole number.")
            return
        
        events = int(text)
        if not 1 <= events <= 15:
            await update.message.reply_text("Events must be between 1 and 15.")
            return

        context.user_data["events"] = events
        context.user_data.pop("step")
        await show_confirmation(update, context)
    
async def show_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data

    sports_display = "All" if not data["sports"] else ", ".join(s.title() for s in data["sports"])

    text = (
        "✅ Confirm Bet Slip Settings\n\n"
        f"Sports: {sports_display}\n"
        f"Time range: {data['time_range']}\n"
        f"Market: {data['market']}\n"
        f"Odds: {data['odd_from']} → {data['odd_to']}\n"
        f"Max events: {data['events']}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Confirm ✅", callback_data="confirm")],
        [InlineKeyboardButton("Cancel ❌", callback_data="cancel")]
    ])

    await update.message.reply_text(text, reply_markup=keyboard)

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        context.user_data.clear()
        await query.message.delete()
        await context.bot.send_message(chat_id=query.message.chat_id, text="Cancelled. Use /generate_bet_slip to start again.")
        return
    
    await query.message.delete()
    await context.bot.send_message(chat_id=query.message.chat_id, text="Generating bet slips…")
    await fetch_bet_slips_from_scores24(query, context)

async def fetch_bet_slips_from_scores24(query, context):
    data = context.user_data
    user_tz = data.get("timezone", "UTC")
    
    payload_copy = json.loads(json.dumps(payload))
    vars = payload_copy["variables"]

    if not data["sports"]:
        vars["sportSlugs"] = []
    else:
        vars["sportSlugs"] = list(data["sports"])
    vars["hours"] = int(data["time_range"].split()[0])
    vars["markets"] = [data["market_converted"]]
    vars["oddFrom"] = data["odd_from"]
    vars["oddTo"] = data["odd_to"]
    vars["events"] = data["events"]

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post('https://scores24.live/graphql', cookies=cookies, headers=headers, json=payload_copy)

    if response.status_code != 200:
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"Scores24 API error, status code: {response.status_code}")
        return

    json_data = response.json()
    trends = json_data.get("data", {}).get("CustomExpress", {}).get("trends", [])
    filtered_trends = []

    for trend in trends:
        match = trend["match"]

        if data["sports"] and match["sportSlug"] not in data["sports"]:
            continue

        match_time = datetime.strptime(match["matchDate"], "%Y-%m-%d %H:%M:%S")
        if match_time > datetime.utcnow() + timedelta(hours=vars["hours"]):
            continue

        if data["market_converted"] != "all":
            if trend["market"]["category"] != data["market_converted"]:
                continue

        odd = pick_best_odd(trend["odds"])
        if not (data["odd_from"] <= odd <= data["odd_to"]):
            continue

        filtered_trends.append(trend)

    filtered_trends = filtered_trends[:data["events"]]

    if not filtered_trends:
        await context.bot.send_message(chat_id=query.message.chat_id, text="No matches found for given filters.")
        return
    
    message = "🎯 Predictions - Today\n\n"

    for trend in filtered_trends:
        message += format_trend_card(trend, user_tz)
        message += "\n────────────────────────────────────────\n\n"

    MAX_LEN = 4000
    for i in range(0, len(message), MAX_LEN):
        await context.bot.send_message(chat_id=query.message.chat_id, text=message[i:i + MAX_LEN])
    context.user_data.clear()

async def error_handler(update, context):
    logging.exception("Unhandled error", exc_info=context.error)

def main():
    print("Booting up the bot")
    application = ApplicationBuilder().token(bot_token).build()
    
    start_handler = CommandHandler("start", start_command)
    location_handler = MessageHandler(filters.LOCATION, handle_location)
    help_handler = CommandHandler("help", help_command)
    contact_handler = CommandHandler("contact", contact_command)

    generate_bet_slip_handler = CommandHandler("generate_bet_slip", generate_bet_slip_command)
    sport_selection_handler = CallbackQueryHandler(handle_sport_selection, pattern="^(sport:|sport_next)")
    time_selection_handler = CallbackQueryHandler(handle_time_range_selection, pattern="^(time_range:|time_next)")
    market_selection_handler = CallbackQueryHandler(handle_market_selection, pattern="^(market:|market_next)")
    numeric_input_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numeric_input)
    confirmation_handler = CallbackQueryHandler(handle_confirmation, pattern="^(confirm|cancel)$")

    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)

    application.add_handler(start_handler)
    application.add_handler(location_handler)
    application.add_handler(help_handler)
    application.add_handler(contact_handler)

    application.add_handler(generate_bet_slip_handler)
    application.add_handler(sport_selection_handler)
    application.add_handler(time_selection_handler)
    application.add_handler(market_selection_handler)
    application.add_handler(numeric_input_handler)

    application.add_handler(confirmation_handler)
    application.add_error_handler(error_handler)
    application.add_handler(unknown_handler)

    print("Bot successfully initialized, now listening for inputs")
    application.run_polling()

if __name__ == '__main__':
    main()