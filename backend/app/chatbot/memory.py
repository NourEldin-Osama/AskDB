import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from app.core.config import settings

conn = sqlite3.connect(settings.memory_db_path, check_same_thread=False)
memory = SqliteSaver(conn)
