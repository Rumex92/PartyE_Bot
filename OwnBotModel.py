import joblib

loaded_pipe = joblib.load('pipeline_model.pkl', mmap_mode='r')

def get_response(question):
    response = loaded_pipe.predict([question])[0]
    return response

# # Function to interact with the user
# def chat():
#     while True:
#         question = input("You: ")
#         if question.lower() == 'quit':
#             print("Chatbot: Goodbye!")
#             break
#         response = get_response(question)
#         print("Chatbot:", response)

# # Start the chat
# chat()