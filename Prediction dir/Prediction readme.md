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


## Setup guide

1. Navigate to the repository's [home page][https://github.com/byte-dev404/Scores24-Scrapers-and-Telegram-Bots.git]

2. Click the star icon if you want to bookmark the project (Recommanded).

3. Click the green `<> Code` button and either:

* Download the ZIP file and extract it, or

* Copy the repository URL and clone it:

```bash
git clone https://github.com/byte-dev404/Linsol-Products-Scraper.git
```

4. Install an IDE such as VS Code: https://code.visualstudio.com/Download

5. Install the latest version of Python for your operating system: https://www.python.org/downloads/

6. Open the cloned or extracted project folder in your IDE.

* For vs code, run the following command from the parent folder where you downloaded/cloned the repo

```bash
code Scores24-Scrapers-and-Telegram-Bots
```

7. Open a terminal:

* Press `` Ctrl + Shift + ` ``
* Or use the menu: Terminal → New Terminal

8. Set Up a Virtual Environment (Recommended):

1. **Create a virtual environment.**
```bash
python -m venv venv
```

2. **Activate virtual environment:**

* For Windows:
```bash
source venv/Scripts/activate
```

* For Mac/Linux:
```bash
source venv/bin/activate
```

9. Install required dependencies:

```bash
pip install -r requirements.txt
```

