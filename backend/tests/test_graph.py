from ai_chat_db.Chatbot import graph

config = {"configurable": {"thread_id": "1"}}
response = graph.invoke({"messages": [{"role": "user", "content": "Hello!"}]}, config)
response_text = response["messages"][-1].content

# print(f"{response = }")
print(f"{response_text = }")
print(f"{response.keys() = }")
