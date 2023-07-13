from revChatGPT.V1 import Chatbot

def GPT_react(prompt):

    # print(f"prompt : {prompt}")
    f = open('token.txt', 'r')

    token = f.read()

    chatbot = Chatbot(config={
        "access_token": token
    })

    response = ""
    for data in chatbot.ask(prompt):
        response = data["message"]
    # print(f"response : {response}")
    return response