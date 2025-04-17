from app.chatbot.chatbot_core import Chatbot

chatbot = Chatbot()

config = {"configurable": {"thread_id": "1"}}
response = chatbot.agent.invoke({"messages": [{"role": "user", "content": "Hello!"}]}, config)
response_text = response["messages"][-1].content

# print(f"{response = }")
print(f"{response_text = }")
print(f"{response.keys() = }")
