from ai_chat_db.Chatbot import tools

for tool in tools:
    print(f"Tool: {tool.name} - {tool.description}")

get_schema_tool = tools[3]
print(get_schema_tool.invoke(input="properties"))  # This will print the schema of the table 'properties'

query_tool = tools[4]
print(query_tool.invoke(input="SELECT * FROM properties"))  # This will print all the data from the 'properties' table
