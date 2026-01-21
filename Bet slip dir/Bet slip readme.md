# Scores24 Bet Builder Scraper and Telegram Bot

This directory contains a powerful Python scraper for the **Scores24 Bet Builder** feature, along with a Telegram bot built on top of it.

The scraper interacts directly with Scores24’s exposed GraphQL endpoint to fetch Bet Builder data and returns raw JSON responses. These responses can be used for multiple purposes. In this repository, the scraper is embedded into a Telegram bot, allowing users to select filters interactively and receive structured bet slips based on their selections.

This README provides a detailed overview of the directory structure, setup process, testing instructions, and a high level explanation of how both the scraper and the bot work.


## Directory Contents

| File or Folder | Description |
| -- | -- |
| `Bet slip readme.md` | Main documentation file for both the Bet Builder scraper and Telegram bot. |
| `requirements.txt` | Lists all Python packages required by the scraper and the bot. |
| `Bet slip scraper.py` | Core scraper script that accepts filter inputs and fetches raw JSON data from Scores24. |
| `Bet slip scraper.exe` | Windows executable version of the scraper for quick testing without any setup. |
| `Bet slip generator bot.py` | Telegram bot script built on top of the scraper. Add your bot token and it is ready to deploy. |


## Setup Guide

1. Navigate to the repository homepage:
   [https://github.com/byte-dev404/Scores24-Scrapers-and-Telegram-Bots](https://github.com/byte-dev404/Scores24-Scrapers-and-Telegram-Bots)

2. Optionally, click the star button to bookmark the project.

3. Click the green **Code** button and either:

   * Download the ZIP file and extract it, or
   * Clone the repository using Git:

   ```bash
   git clone https://github.com/byte-dev404/Scores24-Scrapers-and-Telegram-Bots.git
   ```

4. Install an IDE such as Visual Studio Code:
   [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)

5. Install the latest version of Python for your operating system:
   [https://www.python.org/downloads/](https://www.python.org/downloads/)

6. Open the cloned or extracted project folder in your IDE.

   For VS Code, run the following command from the parent directory:

   ```bash
   code Scores24-Scrapers-and-Telegram-Bots
   ```

7. Open a terminal:

   * Press `Ctrl + Shift + ``
   * Or use the menu: Terminal → New Terminal

8. Set up a virtual environment (recommended):

   Create the virtual environment:

   ```bash
   python -m venv venv
   ```

   Activate it:

   On Windows:

   ```bash
   source venv/Scripts/activate
   ```

   On macOS or Linux:

   ```bash
   source venv/bin/activate
   ```

9. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```


## Running the Scraper

There are two ways to run the Bet Builder scraper.

### Using the Python Script

If you followed the setup steps correctly, run:

```bash
python "Bet slip scraper.py"
```

### Using the Executable

For quick testing without any setup, you can use the Windows executable.

* Open the Bet slip directory in File Explorer
* Double click on `Bet slip scraper.exe`

**Note:** The executable works only on Windows.


## Testing the Scraper

Once the scraper starts, you will see a message like:

```
Use arrow keys to select options ⬇️ ⬆️
```

This indicates that the scraper is running successfully.

You will be prompted to select filters similar to those available on the Scores24 Bet Builder page. After completing the selections, the scraper will create a `raw files` folder inside the Bet slip directory.

This folder contains the raw JSON responses fetched using your selected filters. You can use this data for further processing or analysis.


## How to Test the Telegram Bot

The bot setup is similar to the scraper, but completing the setup is mandatory.

### Step 1: Add Your Bot Token

There are two ways to add the bot token.

#### Option 1: Paste the Token Directly

This is the quickest method, but not recommended for production.

1. Open `Bet slip generator bot.py`
2. Locate and uncomment the line:

   ```python
   # bot_token = "~~Enter~~your~~bot~~token~~here~~"
   ```
3. Replace the placeholder with your actual bot token

Make sure you never commit your bot token to GitHub.

#### Option 2: Use a `.env` File (Recommended)

1. Create a `.env` file in the root directory
2. Add the following line and insert your bot token:

   ```
   BET_SLIP_GENERATOR_BOT_TOKEN=""
   ```
3. Uncomment these lines in `Bet slip generator bot.py`:

   ```python
   # load_dotenv()
   # bot_token = os.getenv("BET_SLIP_GENERATOR_BOT_TOKEN")
   ```


### Step 2: Run the Bot

Run the following command:

```bash
python "Bet slip generator bot.py"
```

If you see a message like:

```
telegram.ext.Application - INFO - Application started
```

the bot has started successfully.


### Step 3: Confirm the Bot Is Running

Open Telegram and send the `/start` command to your bot. If it responds, the bot is working correctly.

You can now deploy the bot or extend it with additional features.


## How the Scraper Works (For Contributors)

The scraper does not rely on rendered HTML. Instead, it communicates directly with Scores24’s exposed GraphQL API.

High level workflow:

1. The scraper starts and prints a confirmation message.
2. It prompts the user to select filters using the `InquirerPy` library.
3. The selected filters are sent as a request to the Scores24 GraphQL endpoint.
4. If the response is successful, the raw JSON is saved in the `raw files` folder.
5. If an error occurs, the scraper prints an appropriate error message with the status code.


## How the Bot Works (For Contributors)

The bot follows the same core logic as the scraper, but replaces terminal input with Telegram interactions using the `python-telegram-bot` library.

Workflow overview:

1. The bot initializes and logs a startup message.
2. When a user runs `/generate_bet_slip`, the bot begins collecting filter inputs.
3. After all required data is collected, the bot confirms the request.
4. It sends a request to the Scores24 GraphQL endpoint using the selected filters.
5. If the response is valid, the bot extracts useful data and sends structured bet slips to the user.
6. If an error occurs, the bot responds with a clear error message.


## License and Usage

* **Non-commercial use:** Free for personal or educational projects.
* **Commercial use:** Please provide credit by linking to this repository or to my [GitHub profile](https://github.com/byte-dev404).


## Contributing

Contributions are welcome.

1. Open an issue to discuss bugs or feature ideas.
2. Follow PEP 8 coding standards.
3. Submit a pull request with a clear description of your changes.


## Contact

If the scraper or bot breaks, needs customization, or if you want help scraping another website, feel free to reach out.

**Email**
[zendiagogamingbusiness@gmail.com](mailto:zendiagogamingbusiness@gmail.com)

**LinkedIn**
[https://www.linkedin.com/in/vishwas-batra/](https://www.linkedin.com/in/vishwas-batra/)