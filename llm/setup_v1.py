from revChatGPT.V1 import Chatbot


class ChatBotRev(object):

    def __init__(self):
        self.chatbot = Chatbot(config={
            "access_token": "<ACCESS_TOKEN>",
            "model": "text-davinci-002-render-paid"
        })

    def ask(self, prompt):
        response = ""
        for data in self.chatbot.ask(prompt):
            response = data["message"]

        return response
