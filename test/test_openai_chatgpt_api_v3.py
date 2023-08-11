from llm.setup_v3 import ChatBotPaid

b = ChatBotPaid()
with open("prompt.txt", "r") as f:
    text = "".join(f.readlines())
    print(b.ask(text))
