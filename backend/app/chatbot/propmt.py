from langchain import hub

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
system_message = prompt_template.format(dialect="SQLite", top_k=5)
