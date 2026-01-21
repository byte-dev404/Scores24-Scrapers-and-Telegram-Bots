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


## Running the scraper

Now, there are two different ways to run the scraper,


### Using the python script:

If you follow the setup guide correctly, then just the following comand in the terminal:

```bash
python "Prediction scraper.py"
```


### Using executable:

if you want to do a quick test without doing all the setup then just follow the steps below to run the executable, but keep in mind that it will only work on windows:

* Open the `Prediction dir` folder in file explorer 
* Double click on the `Prediction scraper.exe` file


### Testing

After you run the scraper no matter which way, you'll see `Use arrow keys to select options ⬇️ ⬆️` in the terminal, it means the scraper has started.

From there, it'll ask give you a few options to choose form, these are basically the filters you find on scores24 website, once you're done with the questionaries, the scraper will generate a `raw files` folder in the `Prediction dir` which contains the raw josn fetched form the filters, you just have selected.

Now, you can use that raw json data to do whatever you want with it. 


## How to test the bot

The process of test the bot is very similar to the scraper.
Just make sure you've done the setup correctly, as it is mandatory for running the bot not optional.

1. Add your bot token.

To run the script you must add your bot token in it, there are two ways to it.

* Paste it in the script:

The most easiest way is to paste your bot taken directly in the script, it is not a best practice but just make sure not never commit you token to github.

1. Locate and uncomment this line `# bot_token = "~~Enter~~your~~bot~~token~~here~~" ` in the `Prediction generator bot.py` file, you'll find it right after imports.
2. Replcae this `"~~Enter~~your~~bot~~token~~here~~"` with your actual bot token string.

* Load bot token from .env

This it the best and recommended way, so you'll never have to worry about accidently leaking your secrets.

1. Create a `.env` file at the root of the directory.
2. Add this line `PREDICTION_GENERATOR_BOT_TOKEN = ""` in .env file and replace the empty string with your bot token.
3. Now uncomment the following lines from `Prediction generator bot.py` found right after imports:
```python
# load_dotenv()
# bot_token = os.getenv("PREDICTION_GENERATOR_BOT_TOKEN")
```

2. Run the bot

Now just paste this command in the terminal:

```bash
python "Prediction generator bot.py"
```
you'll see something like `telegram.ext.Application - INFO - Application started` in the terminal, it indicates that the bot has started sucessfully.

3. Confirm the bot is initialized

Go to your telegram bot and run the /start command, the bot will reponed.

Now you can deploy the bot and add new featues to it as your liking.


## How the scraper works (for contributors)

The scraper is very simple and flexible as it does not rely on the html rendered on Scores24 instead it utilizes the exposed graphQL API.

Here's a workflow so you really understands what's going under the hood.

1. The scraper starts and a confirmation message to indicate it has started. 
2. Then it ask users to select some options from the given choices in the terminal through `inquirerpy` package, which are basically the filters one finds on Scores24 prediction page
3. After the user is done with questionaries, the scraper sends the request with the selcted filters 
4. Finally, if the Scores24 response is ok, then it saves the raw json in `raw files` folder otherwise it prints an error message with the status code of sent by Scores24.

