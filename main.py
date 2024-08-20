import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
from ChatBotModel import get_message
from OwnBotModel import get_response
import message_db

load_dotenv()

TOKEN = os.getenv('TOKEN')
BOT_USERNAME =  os.getenv('BOT_USERNAME')


#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please, type '/help' for help")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Hello, this is an AI class project for LAP.
This bot has two version, advanced bot and dumb bot.

To chat with advanced bot 
/adv

To chat with dumb bot
/dumb

To look at the info of each bot 
/dumb_info or /adv_info

    (advanced bot is set as default)
        """
    )


async def adv_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_db.save_bot_type(user_id, 1)  # 1 represents the advanced bot
    await update.message.reply_text("Changed to advanced bot.")


async def dumb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_db.save_bot_type(user_id, 2)  # 2 represents the dumb bot
    await update.message.reply_text("Changed to dumb bot.")


async def dumb_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # add code
    pass


async def adv_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # add code
    pass



# for debugging
async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    history = message_db.get_history(user_id)
    
    if not history:
        response = "No message history found."
    else:
        response = message_db.get_history(user_id)

    await update.message.reply_text(response)


async def type_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    botType = message_db.get_bot_type(user_id)
    await update.message.reply_text(botType)


#responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_type = update.message.chat.type
    text = update.message.text
    bot_type = message_db.get_bot_type(user_id)
    user_history = message_db.get_history(user_id)

    if message_type == 'group':
        return
    else:
        await update.message.chat.send_action(ChatAction.TYPING)
        if bot_type == 2: 
            # to add dumb bot 
            response = get_response(text) #this is from ownbot
        else:
            response = get_message(text,  user_history) #this is from dumb bot
            message_db.save_history(user_id, user_history)
        await update.message.reply_text(response)


if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('adv', adv_command))
    app.add_handler(CommandHandler('dumb', dumb_command))
    app.add_handler(CommandHandler('adv_info', adv_info_command))
    app.add_handler(CommandHandler('dumb_info', dumb_info_command))

    # for debugging
    app.add_handler(CommandHandler('history', history_command))
    app.add_handler(CommandHandler('type', type_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling(poll_interval=3)