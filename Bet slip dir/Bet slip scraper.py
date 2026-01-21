import os
import json
import requests
from InquirerPy import inquirer


json_dir = os.path.join("Bet slip dir", "raw files")
os.makedirs(json_dir, exist_ok=True)

bet_slip_endpoint = "https://scores24.live/graphql"

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

# Default params
sport = []
time_range = 2
event = 15
market = 'all'
odd_from = 1.1
odd_to = 2.9

# All options
sports_options = ['all', 'soccer', 'basketball', 'tennis', 'ice-hockey', 'table-tennis', 'volleyball', 'handball', 'baseball', 'american-football', 'rugby', 'cricket', 'mma', 'boxing', 'snooker', 'futsal', 'waterpolo', 'badminton', 'darts', 'csgo', 'dota2', 'lol', 'horse-racing',]
time_options = ['2 hours', '6 hours', '12 hours', '24 hours', '48 hours']
market_options = ['All', 'Match Result', 'Double Chance', 'Over/Under', 'Correct Score', 'Both Teams to Score', 'Handicap', 'Corners', 'Fouls', 'Cards', 'Shots', 'Off-sides']
market_options_translation = {
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


def main():
    print("\nUse arrow keys to select options ⬇️ ⬆️\n")

    selected_sport = inquirer.select(message="Select a sport: ", choices=sports_options, max_height=len(sports_options)).execute()
    selected_time = inquirer.select(message="Select a time for the freshness of results: ", choices=time_options, height=len(time_options)).execute()
    selected_event = input('Choose the number of events between 1 to 15 (Defaults to 15) : ')
    selected_market = inquirer.select(message='Select a market: ', choices=market_options, height=(len(market_options))).execute()
    selected_oddFrom = input('Enter a value between 1.1 to 2.9 for Odd-From (Defaults to 1.1): ')
    selected_oddTo = input(f'Enter a value between {selected_oddFrom or 1.2} to 3.0 for Odd-To (Defaults to 3.0): ')


    if selected_sport != "all":
        sport = [selected_sport]

    time_range = int(selected_time.split(' ')[0])

    selected_event = int(selected_event) 
    if selected_event > 1 and selected_event < 15:
        event = selected_event

    market = market_options_translation[selected_market]

    if selected_oddFrom:
        selected_oddFrom = float(selected_oddFrom)

        if selected_oddFrom > 1.1 and selected_oddFrom < 2.9:
            odd_from = selected_oddFrom
            
    if selected_oddTo:
        selected_oddTo = float(selected_oddTo)
        
        if selected_oddTo > odd_from and selected_oddTo < 3.0:
            odd_to = selected_oddTo

    print(f"""
Here's what you choose:
  Sport: {sport}
  Time: {time_range} hours
  Event: {event}
  Market: {market}
  Odd-From: {odd_from}
  Odd-To: {odd_to}
""")

    json_data_for_custom_results = {
        'operationName': 'CustomAccumFeed',
        'query': 'query CustomAccumFeed($sportSlugs: [String], $leagueSlugs: [String], $hours: Int, $events: Int, $markets: [String], $oddFrom: Float, $oddTo: Float, $langSlug: String!, $couponKey: String, $excludeIds: [String], $audience: String!) {\n  CustomExpress(\n    sport_slugs: $sportSlugs\n    leagues: $leagueSlugs\n    hours: $hours\n    events: $events\n    markets: $markets\n    odd_from: $oddFrom\n    odd_to: $oddTo\n    lang: $langSlug\n    couponKey: $couponKey\n    exclude_ids: $excludeIds\n    audience: $audience\n  ) {\n    ...AccumFragment\n    resetIds: reset_ids\n    trends {\n      ...AccumTrendFragment\n      __typename\n    }\n    bookmakers {\n      ...AccumBookmakerFragment\n      __typename\n    }\n    legalBookmakers: legal_bookmakers {\n      langSlug: lang_slug\n      name\n      slug\n      logo\n      color\n      favicon\n      bonus\n      bonusCurrency: bonus_currency\n      hasPromotions: has_promotions\n      bonusTypeName: bonus_type_name\n      __typename\n    }\n    __typename\n  }\n}\nfragment AccumFragment on ExpressCoupon {\n  langSlug: lang_slug\n  section\n  couponKey: coupon_key\n  sportSlug: sport_slug\n  marketCategory: market_category\n  hasLegal: has_legal\n  probability\n  rate\n  __typename\n}\nfragment AccumTrendFragment on ExpressTrend {\n  id\n  groupedFacts: grouped_facts {\n    title\n    facts {\n      fact\n      text\n      team {\n        ...TeamCacheFragment\n        logo\n        __typename\n      }\n      referee {\n        ...RefereeCacheFragment\n        logo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  factsCount: facts_count\n  length\n  priority\n  rate\n  market {\n    category\n    type\n    subtype\n    __typename\n  }\n  match {\n    ...MatchCacheFragment\n    type\n    leagueSlug: league_slug\n    sportSlug: sport_slug\n    uniqueTournamentName: unique_tournament_name\n    tournament: unique_tournament {\n      ...LeagueCacheFragment\n      name\n      __typename\n    }\n    teams {\n      ...TeamCacheFragment\n      logo\n      name\n      country {\n        iso\n        __typename\n      }\n      __typename\n    }\n    country {\n      ...CountryFragment\n      __typename\n    }\n    __typename\n  }\n  bookmakerSlug: bookmaker_slug\n  odds {\n    bookmakerSlug: bookmaker_slug\n    odd\n    __typename\n  }\n  __typename\n}\nfragment TeamCacheFragment on Team {\n  slug\n  langSlug: lang_slug\n  name\n  temporarilyQualified: temporarily_qualified\n  __typename\n}\nfragment RefereeCacheFragment on Referee {\n  slug\n  name\n  langSlug: lang\n  __typename\n}\nfragment MatchCacheFragment on Match {\n  slug\n  matchDate: match_date\n  langSlug: lang_slug\n  __typename\n}\nfragment LeagueCacheFragment on League {\n  slug\n  langSlug: lang_slug\n  sportSlug: sport_slug\n  __typename\n}\nfragment CountryFragment on Country {\n  name\n  slug\n  iso\n  __typename\n}\nfragment AccumBookmakerFragment on ExpressBookmaker {\n  bookmaker {\n    langSlug: lang_slug\n    name\n    slug\n    logo\n    color\n    favicon\n    bonus\n    bonusCurrency: bonus_currency\n    hasPromotions: has_promotions\n    bonusTypeName: bonus_type_name\n    __typename\n  }\n  slug\n  rate\n  probability\n  __typename\n}',
        'variables': {
            'audience': 'us',
            'couponKey': 'custom',
            'events': event,
            'excludeIds': [],
            'hours': time_range,
            'langSlug': 'en',
            'leagueSlugs': [],
            'markets': market,
            'oddFrom': odd_from,
            'oddTo': odd_to,
            'sportSlugs': sport,
        },
    }

    response = requests.post(bet_slip_endpoint, cookies=cookies, headers=headers, json=json_data_for_custom_results)

    print(response.status_code)

    if response.status_code == 200:
        file_path = os.path.join(json_dir, "test-1.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)

        print("Success! File saved as test-1.json")
        print("Check if there's a 'test-1.json' file appears in the scraper folder")
    else:
        print("Request failed! Status code:", response.status_code)

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()