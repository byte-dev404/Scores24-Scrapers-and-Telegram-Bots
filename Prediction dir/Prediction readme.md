# Scores 24 Prediction's Scraper and Telegram bot script

Prediction directory of this repository contains strong python scraper that utilizes Scores24's exposed graphQL endpoint to fetch results from Predictions page and returns raw json data, which then can be used for various perposes, like I embeded the scraper in telegram bot script, so now it can ask users for filters and fetch raw json based on those filters and return structured Prediction slips.

This was just an overview, this readme will dive you through the directory structure, scraper and bot's testing process along with how they work on a core level.


## directory contents

| File/Folder | Description |
| -- | -- |
| `Prediction readme.md` | This is the main entry point for both Prediction scraper and bot. |
| `requirements.txt` | This file contains a list of all packages and libraries the scraper and bot relies on, and will be used in the initial setup. |
| `Prediction scraper.py` | The main scraper, it take filter inputs to produces a raw json file and the bot is comprise of it. |
| `Prediction scraper.exe` | It's the windows executable version of the bet slip scraper built for easier testing and requires no setup whatsoever. |
| `Prediction generator bot.py` | The main telegram bot script, built upon prediction scraper, enter your bot token and it's ready to be deployed. |

