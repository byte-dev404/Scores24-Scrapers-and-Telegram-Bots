# Scores24 Prediction Scraper and Telegram Bot

This directory contains a Python scraper for the **Scores24 Predictions** feature, along with a Telegram bot built on top of it.

The scraper communicates directly with Scores24’s exposed GraphQL endpoint to fetch prediction data from the Predictions page and returns raw JSON responses. This data can be reused for multiple purposes. In this repository, the scraper is integrated into a Telegram bot that allows users to apply filters, fetch prediction data, and receive structured prediction slips directly in Telegram.

This README provides a complete overview of the directory structure, setup process, testing instructions, and a high level explanation of how both the scraper and the bot work internally.


## Directory Contents

| File or Folder | Description |
| -- | -- |
| `Prediction readme.md`        | Main documentation entry point for both the Prediction scraper and the Telegram bot.       |
| `requirements.txt`            | Lists all Python dependencies required by the scraper and the bot.                         |
| `Prediction scraper.py`       | Core scraper script that accepts filter inputs and fetches raw JSON prediction data.       |
| `Prediction scraper.exe`      | Windows executable version of the scraper for quick testing without setup.                 |
| `Prediction generator bot.py` | Telegram bot script built on top of the prediction scraper. Add your bot token and deploy. |


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

There are two ways to run the prediction scraper.

### Using the Python Script

If the setup was completed correctly, run:

```bash
python "Prediction scraper.py"
```

### Using the Executable

For quick testing without setup, you can use the Windows executable.

* Open the Prediction directory in File Explorer
* Double click on `Prediction scraper.exe`

Note: The executable works only on Windows.


## Testing the Scraper

After the scraper starts, you will see:

```
Use arrow keys to select options ⬇️ ⬆️
```

This indicates that the scraper is running successfully.

You will be prompted to select filters similar to those available on the Scores24 Predictions page. Once the selections are complete, the scraper will create a `raw files` folder inside the Prediction directory.

This folder contains the raw JSON responses fetched using your selected filters. You are free to process or reuse this data as needed.


## How to Test the Telegram Bot

The bot setup process is similar to the scraper, but completing the setup is mandatory.

### Step 1: Add Your Bot Token

There are two supported ways to add the bot token.

#### Option 1: Paste the Token Directly

This is the fastest method, but not recommended for production use.

1. Open `Prediction generator bot.py`
2. Locate and uncomment the line:

   ```python
   # bot_token = "~~Enter~~your~~bot~~token~~here~~"
   ```
3. Replace the placeholder with your actual bot token

Make sure the token is never committed to GitHub.

#### Option 2: Use a `.env` File (Recommended)

1. Create a `.env` file in the root directory
2. Add the following line and insert your bot token:

   ```
   PREDICTION_GENERATOR_BOT_TOKEN=""
   ```
3. Uncomment these lines in `Prediction generator bot.py`:

   ```python
   # load_dotenv()
   # bot_token = os.getenv("PREDICTION_GENERATOR_BOT_TOKEN")
   ```


### Step 2: Run the Bot

Run the following command:

```bash
python "Prediction generator bot.py"
```

If you see:

```
telegram.ext.Application - INFO - Application started
```

the bot has started successfully.


### Step 3: Confirm the Bot Is Running

Open Telegram and send the `/start` command to your bot. If the bot responds, it is working correctly.

You can now deploy the bot or extend it with additional features.


## How the Scraper Works (For Contributors)

The scraper does not rely on rendered HTML. Instead, it communicates directly with Scores24’s exposed GraphQL API.

Workflow overview:

1. The scraper starts and logs a confirmation message.
2. It prompts the user to select filters using the `InquirerPy` library.
3. The selected filters are sent to the Scores24 GraphQL endpoint.
4. If the response is successful, the raw JSON is saved in the `raw files` folder.
5. If an error occurs, the scraper prints a clear error message with the response status code.


## How the Bot Works (For Contributors)

The bot follows the same core logic as the scraper, but replaces terminal input with Telegram interactions using the `python-telegram-bot` library.

Workflow overview:

1. The bot initializes and logs a startup message.
2. When a user runs `/generate_predictions`, the bot begins collecting filter inputs.
3. Once all required data is collected, the bot sends a confirmation message.
4. The bot sends a request to the Scores24 GraphQL endpoint using the selected filters.
5. If the response is valid, the bot extracts useful data and sends structured prediction slips to the user.
6. If an error occurs, the bot responds with an appropriate error message.


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