import openai
import telegram
import os
import sqlite3
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set Telegram token
bot = telegram.Bot(token=os.environ.get("TELEGRAM_TOKEN"))
updater = Updater(token=os.environ.get("TELEGRAM_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to or create a SQLite database to store previous messages
try:
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    # Create a table to store previous messages
    c.execute('''CREATE TABLE IF NOT EXISTS messages (message text, timestamp timestamp)''')
except sqlite3.Error as e:
    logging.error(e)
    print(e)

def reply_openai(update, context):
    # Get user message
    message = update.message.text
    try:
        # Fetch previous messages
        c.execute('SELECT message FROM messages ORDER BY timestamp DESC')
        prev_messages = c.fetchall()
        prev_messages = "\n".join([row[0] for row in prev_messages])
        # Use OpenAI to generate a response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{message}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            context=f"Previous messages: {prev_messages}")
        if "choices" in response:
            # Send response to user
            context.bot.send_message(chat_id=update.message.chat_id, text=response["choices"][0]["text"])
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I am unable to understand your query.")
        # Store the message in the SQLite database
        c.execute("INSERT INTO messages VALUES (?, datetime('now'))", (message,))
        conn.commit()
    except openai.exceptions.OpenAiError as e:
        if e.status_code == 429:
            time.sleep(int(e.headers["Retry-After"]))
            reply_openai(update, context)
        else:
            logging.error(e)
            context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, something went wrong. Please try again later.")

# Handle all text messages
text_handler = MessageHandler(Filters.text, reply_openai)
dispatcher.add_handler(text_handler)

# Handle the /help command
def help_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I am a bot that uses the OpenAI API to respond to your messages. You can send me any message and I will try my best to respond.\nType /stop to stop the bot.")

help_handler = CommandHandler("help", help_command)
dispatcher.add_handler(help_handler)

# Handle the /stop command
def stop_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Stopping bot.")
    updater.stop()

stop_handler = CommandHandler("stop", stop_command)
dispatcher.add_handler(stop_handler)

# Handle the /clear command
def clear_command(update, context):
    c.execute("DELETE FROM messages")
    conn.commit()
    context.bot.send_message(chat_id=update.message.chat_id, text="Previous messages cleared.")

clear_handler = CommandHandler("clear", clear_command)
dispatcher.add_handler(clear_handler)

# Start the bot
updater.start_polling()