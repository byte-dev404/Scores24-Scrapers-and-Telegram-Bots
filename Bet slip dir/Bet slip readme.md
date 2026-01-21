# Scores 24 Bet Builder's Scraper and Telegram bot script

Bet slip diractory of this repository contains strong python scraper that utilizes Scores24's exposed graphQL endpoint to fetch results from Bet builder page and returns raw json data, which then can be used for various perposes, like I embeded the scraper in telegram bot script, so now it can ask users for filters and fetch raw json based on those filters and return structured bet-slips.

This was just an overview, this readme will dive you through the diractory structure, scraper and bot's testing process along with how they work on a core level.


## Diractory contents

| File/Folder | Description |
| -- | -- |
| `Bet slip readme.md` | This is the main entry point for both bet builder scraper and bot. |
| `requirements.txt` | This file contains a list of all packages and libraries the scraper and bot relies on, and will be used in the initial setup. |
| `Bet slip scraper.py` | The main scraper, it take filter inputs to produces a raw json file and the bot is comprise of it. |
| `Bet slip scraper.exe` | It's the windows executable version of the bet slip scraper built for easier testing and requires no setup whatsoever. |
| `Bet slip generator bot.py` | The main telegram bot script, built upon bet slip scraper, enter your bot token and it's ready to be deployed. |
