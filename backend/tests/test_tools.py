from ai_chat_db.Chatbot import tools

for tool in tools:
    print(f"Tool: {tool.name} - {tool.description}")

print("Testing tools...")
get_tables_tool = tools[2]
print("Tables: ", get_tables_tool.invoke(input=""))  # This will print all the tables in the database

print("Testing get_schema...")
get_schema_tool = tools[3]
print(get_schema_tool.invoke(input="properties"))  # This will print the schema of the table 'properties'

print("Testing query_data...")
query_tool = tools[4]
print(query_tool.invoke(input="SELECT * FROM properties"))  # This will print all the data from the 'properties' table
