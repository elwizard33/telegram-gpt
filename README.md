Telegram OpenAI Bot
===================

This script is a Telegram bot that uses the OpenAI API to generate responses to user input. It is built using Python and several libraries, including the `openai`, `telegram`, and `sqlite3` libraries.

How it works
------------

1.  The script starts by setting the OpenAI API key and Telegram token using the `os` library to access environment variables.
2.  Next, it creates a connection to a local SQLite database to store previous messages. If the database does not exist, it creates a new one and creates a table to store messages.
3.  Then, it sets up Telegram bot and message handlers using the `telegram` library, which allows the bot to listen for incoming messages and execute specific actions based on the message's content.
4.  When a user sends a message to the bot, the script uses the `openai` library to generate a response. It first fetches previous messages from the SQLite database and uses them as context for the OpenAI model.
5.  Then, it sends the response back to the user and stores the message in the SQLite database.
6.  The script also includes command handlers for the `/help`, `/stop` and `/clear` command, which allows the user to get help, stop the bot and clear the previous messages.

Requirements
------------

-   Python 3
-   openai library
-   telegram library
-   sqlite3 library

Running the script
------------------

1.  Clone the repository
2.  Install the required libraries by running `pip install -r requirements.txt`
3.  Set the `OPENAI_API_KEY` and `TELEGRAM_TOKEN` environment variables
4.  Run the script with `python start.py`

Note: Make sure you have a Telegram bot created and the token is set in the environment variable.

Customization
-------------

The script is designed to be easily customizable. You can change the OpenAI model used, the maximum number of tokens generated, the temperature, and other parameters to suit your needs.

You can also add new functionalities, like handling images, videos, audio etc.

Conclusion
----------

This script is a good starting point for building a Telegram bot that uses the OpenAI API to generate responses to user input. With a few modifications, it can be used to build a wide range of bots with different functionality.
