import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
from ChatBotModel import get_message

load_dotenv()

TOKEN = os.getenv('TOKEN')
BOT_USERNAME =  os.getenv('BOT_USERNAME')

user_botType = {}
user_histories = {}

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
    user_botType[user_id] = 1  # 1 represents the advanced bot
    await update.message.reply_text("Changed to advanced bot.")


async def dumb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_botType[user_id] = 2  # 2 represents the dumb bot
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
    history = user_histories[user_id]
    
    if not history:
        response = "No message history found."
    else:
        response = user_histories[user_id]

    await update.message.reply_text(response)


async def type_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    botType = user_botType[user_id]  
    await update.message.reply_text(botType)


#responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == 'group':
        return
    else:
        if user_id not in user_histories:
            user_histories[user_id] = []

        await update.message.chat.send_action(ChatAction.TYPING)
        response = get_message(text,  user_histories[user_id])
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