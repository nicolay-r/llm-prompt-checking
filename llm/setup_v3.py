from revChatGPT.V3 import Chatbot


class ChatBotPaid(object):

    def __init__(self):
        self.chatbot = Chatbot(
            engine="gpt-4-0314",
            api_key="<API-KEY>")

    def ask(self, prompt):
        return self.chatbot.ask(prompt)
