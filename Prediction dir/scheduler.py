import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

sys.path.insert(0, "/home/container/.local")
import json
import logging
from curl_cffi.requests import AsyncSession
from telegram import Bot

predictions_endpoint = "https://scores24.live/graphql"

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

config_file = "config.json"

scheduler = AsyncIOScheduler()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_scheduler_running():
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started dynamically")

def load_config():
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception:
        logger.exception("Failed to load config")
        return {}

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
    
    return extract_predictions(response.json(), config.get("min_confidence"))

async def run_scheduled_job(bot: Bot, channel_id: int, config: dict):
    try:
        predictions = await fetch_predictions_core(config)

        if not predictions:
            logger.info(f"No predictions for channel {channel_id}")
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

            await bot.send_message(chat_id=channel_id, text=prediction_msg, disable_web_page_preview=True)
        logger.info("Scheduler: predictions posted successfully")

    except Exception:
        logger.exception(f"Scheduler job failed for {channel_id}")

def add_channel_jobs(bot: Bot, channel_id: int, config: dict):
    if not config.get("enabled"):
        return
    
    ensure_scheduler_running()
    
    for t in config.get("post_times", []):
        hour, minute = map(int, t.split(":"))

        scheduler.add_job(
            run_scheduled_job,
            CronTrigger(hour=hour, minute=minute),
            args=[bot, channel_id, config],
            id=f"{channel_id}_{hour}_{minute}",
            replace_existing=True
        )

        logger.info(f"Dynamically scheduled {channel_id} at {hour:02d}:{minute:02d}")


def schedule_jobs(bot: Bot):
    ensure_scheduler_running()
    all_configs = load_config()

    if not all_configs:
        logger.info("No scheduled configs found")
        return
    
    for channel_id_str, config in all_configs.items():
        if not config.get("enabled"):
            continue

        channel_id = int(channel_id_str)
        times = config.get("post_times", [])

        for t in times:
            hour, minute = map(int, t.split(":"))

            scheduler.add_job(
                run_scheduled_job,
                CronTrigger(hour=hour, minute=minute),
                args=[bot, channel_id, config],
                id=f"{channel_id}_{hour}_{minute}",
                replace_existing=True
            )

            logger.info(f"Scheduled {channel_id} at {hour:02d}:{minute:02d}")

    # scheduler.start()