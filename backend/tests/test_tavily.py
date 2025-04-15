from langchain_community.tools.tavily_search import TavilySearchResults

from app.core.config import settings

search_query = "What is LangGraph?"
tavily_search = TavilySearchResults(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)
search_docs = tavily_search.invoke(search_query)
print("Search results for", search_query, ":", search_docs)
