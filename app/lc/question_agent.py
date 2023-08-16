from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from app.lc.sdk import llm


PROMPT = """
  You are an assistant named Skuup. Your job is to assist users with their questions about local events.
  The events can generally fall into one of the following categories: hospitality, cultural events, shopping, venue events, and communtiy events.
"""

tools = [
    # Tool(
    #     name = "Current Search",
    #     func=search.run,
    #     description="useful for when you need to answer questions about current events or the current state of the world"
    # ),
]


# memory = ConversationBufferMemory(memory_key="chat_history")


def question_agent(question, conversation):

    history = ChatMessageHistory()
    for message in conversation:
        history.add_user_message(message['user_message'])
        history.add_ai_message(message['ai_message'])
    print('history', history)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=history,
        ai_prefix="Skuup",
        human_prefix="user",
        output_key="output",
    )

    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    return agent_chain.run(question)
