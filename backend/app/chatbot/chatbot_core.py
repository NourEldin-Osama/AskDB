from langgraph.prebuilt import create_react_agent

from app.chatbot.memory import chat_memory
from app.chatbot.model import model
from app.chatbot.propmt import system_message
from app.chatbot.tools import tools
from app.chatbot.utils import render_markdown_to_html


class Chatbot:
    """Encapsulates the chatbot functionality."""

    def __init__(self):
        self.agent = create_react_agent(model, tools, checkpointer=chat_memory, prompt=system_message)

    def stream_graph_updates(self, user_input: str, thread_id: str) -> None:
        """
        Stream chatbot responses for a given user input and thread.
        Prints each message as it is generated.
        """
        config = {"configurable": {"thread_id": thread_id}}
        for event in self.agent.stream(
            {"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"
        ):
            event["messages"][-1].pretty_print()

    def process_message(self, message: str, thread_id: str) -> str:
        """
        Process a user message and return the chatbot's response as HTML.
        """
        config = {"configurable": {"thread_id": thread_id}}
        response = self.agent.invoke({"messages": [{"role": "user", "content": message}]}, config)
        response_message = response["messages"][-1].content
        return render_markdown_to_html(response_message)


def main() -> None:
    """Run the chatbot in interactive CLI mode."""
    print("Welcome to the AI Chatbot! Type 'quit' or 'exit' to end the conversation.")
    print("You can ask questions or request information about properties and clients.")
    chatbot = Chatbot()
    thread_id = "3"
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in {"quit", "exit", "q"}:
                print("Goodbye!")
                break
            chatbot.stream_graph_updates(user_input, thread_id)
        except Exception as error:
            print(f"An error occurred: {error}")
            break


if __name__ == "__main__":
    main()
