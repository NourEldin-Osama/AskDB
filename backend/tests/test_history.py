from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.chatbot.chatbot_core import Chatbot

# from uuid import uuid4

chatbot = Chatbot()
thread_id = "dbc98a67-591a-4f7f-8654-55e7ae8db4c0"
# thread_id = str(uuid4())
config = {"configurable": {"thread_id": thread_id}}
messages = chatbot.agent.get_state(config).values.get("messages")
if messages:
    for message in messages:
        if isinstance(message, HumanMessage):
            print("User:", end=" ")
        elif isinstance(message, AIMessage):
            if message.tool_calls:
                # print("Tool:", message.tool_calls[0]["name"], end="\n\n")
                continue
            print("AI:", end=" ")
        elif isinstance(message, ToolMessage):
            # print("Tool:", message.name, end="\n")
            # print(message.content)
            continue
        else:
            # Handle other message types if necessary
            print("Other:", type(message).__name__, end=" ")
        print(message.content, end="\n\n")
