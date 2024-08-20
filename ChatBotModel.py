#!/usr/bin/env python
# coding: utf-8

# In[1]:


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# In[2]:


model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


# In[3]:
conversation_history = []



def generate_response(input_text):
   
    if len(conversation_history) > 8:
        conversation_history.pop(0)
        conversation_history.pop(0)
  
    conversation_history.append(input_text)

    history_string = "\n".join(conversation_history)
    inputs = tokenizer.encode_plus(history_string, return_tensors="pt")

    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    conversation_history.append(response)
    
    return response

# input_text = "hello"
# response = generate_response(input_text)
# print("Bot:", response)


# # In[4]:


# input_text = "how are you?"
# response = generate_response(input_text)
# print("ChatBot:", response)


# In[ ]:


# print("Start chatting with the bot (type 'exit' to stop):")
# while True:
  
#     user_input = input("You: ")
    
#     if user_input.lower() == 'exit':
#         print("Chatbot: Goodbye!")
#         break
   
#     bot_response = generate_response(user_input)
#     print("Chatbot:", bot_response)


# In[ ]:
#for telegram

def get_message(text, history):
    if len(history) > 8:
        history.pop(0)
        history.pop(0)
  
    history.append(text)

    history_string = "\n".join(history)
    inputs = tokenizer.encode_plus(history_string, return_tensors="pt", max_length=128)

    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    history.append(response)
    
    return response
