import os
import json
import requests
from InquirerPy import inquirer


json_dir = os.path.join("Prediction generator", "raw files")
os.makedirs(json_dir, exist_ok=True)

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

# Default/Best params
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

# All options
mode_options = ["Best", "Custom"]
time_options = ["all", "today", "tomorrow"]
sport_options = ["all", 'soccer', 'ice-hockey', 'basketball', 'tennis', 'futsal', 'mma', 'snooker', 'baseball', 'american-football', 'csgo', 'volleyball', 'rugby', 'handball', 'boxing',]


def main():
    print("\nUse arrow keys to select options ⬇️ ⬆️\n")

    selected_mode = inquirer.select(message="Select prediction mode: ", choices=mode_options, max_height=len(mode_options)).execute()

    if selected_mode == "Custom":
        selected_time = inquirer.select(message="Select predictions time: ", choices=time_options, max_height=len(time_options)).execute()
        selected_sport = inquirer.select(message="Select sports", choices=sport_options, max_height=len(sport_options)).execute()

        if selected_time != "all":
            json_data["variables"]["day"] = selected_time
        
        if selected_sport != "all":
            json_data["variables"]["sportSlugs"] = [selected_sport,]

        print(f"""
Here's what you choose:
  Mode: {selected_mode}
  Time: {selected_time}
  Sports: {selected_sport}
""")
        
        print("Generating custom predictions...")
        
    if selected_mode == "Best":
        print("Generating best predictions...")

    response = requests.post(url=predictions_endpoint, cookies=cookies, headers=headers, json=json_data)

    if response.status_code == 200:
        file_path = os.path.join(json_dir, "test_1.json")

        with open (file_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)

        print("Success! File saved as test-1.json")
        print("Check if there's a 'test-1.json' file appears in the scraper folder")
    else:
        print("Request failed! Status code:", response.status_code)

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

