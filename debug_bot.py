import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from collections import defaultdict
from userID import handle_message as userID_handle_message, user_histories as userID_histories

load_dotenv()

TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await userID_handle_message(update, context)

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    history = userID_histories.get(user_id, [])
    
    if not history:
        response = "No message history found."
    else:
        history_messages = "\n".join(
            [f"User: {entry['message']}" if entry['from_user'] else f"Bot: {entry['message']}" for entry in history]
        )
        response = f"Your message history:\n{history_messages}"

    await update.message.reply_text(response)

def main():
    logging.info('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('history', history_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()
