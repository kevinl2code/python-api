from langchain.chat_models import ChatOpenAI

from dotenv import dotenv_values

config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                 temperature=0, model="gpt-3.5-turbo-16k")
