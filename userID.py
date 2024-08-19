from collections import defaultdict
from telegram import Update
from telegram.ext import ContextTypes
from ChatBotModel import get_message

user_states = {}
user_histories = defaultdict(list)  

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    message_type = update.message.chat.type
    text = update.message.text

    user_histories[user_id].append({"message": text, "from_user": True})

    if message_type == 'group':
        return
    else:  
       

        if user_id in user_states:
            if user_states[user_id]['waiting_for_response']:
                new_answer = text.strip()
                if new_answer.lower() != 'skip':
                    
                    get_message(user_states[user_id]['unanswered_question'], new_answer)
                    response = 'Thank you! I learned a new response!'
                else:
                    response = 'Okay, no worries!'
                
                user_states[user_id]['waiting_for_response'] = False
            else:
                
                best_response = get_message(text)
                if best_response:
                    response = best_response
                else:
                    response = "I don't know the answer. Can you teach me? Type your response or 'skip' to skip."
                    user_states[user_id] = {'waiting_for_response': True, 'unanswered_question': text}
        else:
            best_response = get_message(text)
            if best_response:
                response = best_response
            else:
                response = "I don't know the answer. Can you teach me? Type your response or 'skip' to skip."
                user_states[user_id] = {'waiting_for_response': True, 'unanswered_question': text}

        user_histories[user_id].append({"message": response, "from_user": False})

        await update.message.reply_text(response)
