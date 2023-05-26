from langchain.chat_models import ChatGooglePalm

from langchain.schema import (
    HumanMessage,
)

if __name__ == "__main__":
    chat = ChatGooglePalm()
    res = chat(messages=[HumanMessage(content="write me a poem about trees")])
    print(res)
