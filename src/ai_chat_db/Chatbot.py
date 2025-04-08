import sqlite3
from typing import Annotated

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from ai_chat_db.config import settings

model_list = [
    "gemini-2.5-pro-exp-03-25",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]

model_name = model_list[0]

search_tool = TavilySearchResults(max_results=2, tavily_api_key=settings.tavily_api_key)
search_tool.name = "search_tool"
search_tool.description = "Search for relevant information in the internet."

conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

database = sqlite3.connect("realestate.db", check_same_thread=False)


@tool
def sum_tool(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


@tool
def get_tables() -> str:
    """Get all the tables in the database"""
    tables = database.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = []
    for table in tables:
        table_name = table[0]
        if table_name:
            table_names.append(table_name)
    return ", ".join(table_names)


@tool
def get_schema(table_name: str) -> str:
    """Get the schema of the specified table."""
    schema = database.execute(f"SELECT sql FROM sqlite_master WHERE name='{table_name}'").fetchone()

    return schema[0] if schema else "Table not found."


@tool
def query_data(sql: str) -> str:
    """Execute SQL queries safely"""
    try:
        result = database.execute(sql).fetchall()
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"Error: {e}"


tools = [search_tool, sum_tool, get_tables, get_schema, query_data]

model = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=settings.google_api_key,
)
model_with_tools = model.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": [model_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile(checkpointer=memory)


def stream_graph_updates(user_input: str, thread_id: str = "1"):
    config = {"configurable": {"thread_id": thread_id}}
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"):
        event["messages"][-1].pretty_print()


if __name__ == "__main__":
    print("Welcome to the AI Chatbot! Type 'quit' or 'exit' to end the conversation.")
    print("You can ask questions or request information about properties and clients.")
    thread_id = "3"
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input, thread_id)
        except Exception as error:
            print(f"An error occurred: {error}")
            # fallback if input() is not available
            break
