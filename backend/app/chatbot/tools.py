from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.chatbot.model import model
from app.core.config import settings


def get_database_engine():
    """Get the database engine for SQLite."""
    return create_engine(
        f"sqlite:///{settings.chatbot_db_file}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


engine = get_database_engine()
database = SQLDatabase(engine)


database_toolkit = SQLDatabaseToolkit(db=database, llm=model)

database_tools = database_toolkit.get_tools()

search_tool = TavilySearchResults(max_results=2, tavily_api_key=settings.TAVILY_API_KEY)
search_tool.name = "search_tool"
search_tool.description = "Search for relevant information in the internet."


tools = [search_tool, *database_tools]
