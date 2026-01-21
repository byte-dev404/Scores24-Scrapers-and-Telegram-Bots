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


## Running the scraper

Now, there are two different ways to do run the scraper,


### Using the python script:

If you follow the setup guide correctly, then just the following comand in the terminal:

```bash
python "Bet slip scraper.py"
```


### Using executable:

if you want to do a quick test without doing all the setup then just follow the steps below to run the executable, but keep it mind that it will only work on windows:

* Open the `Bet slip dir` folder in file explorer 
* Double click on the `Bet slip scraper.exe` file


### Testing

After you run the scraper no matter which way, you'll see `Use arrow keys to select options ⬇️ ⬆️` in the terminal, it means the scraper has started.

From there, it'll ask give you a few options to choose form, these are basically the filters you find on scores24 website, once you're done with the quernaries, the scraper will generate a `raw files` folder in the `Bet slip dir` which contains the raw josn fetched form the filters, you just have selected.

Now, you can use that raw json data to do whatever you want with it. 

