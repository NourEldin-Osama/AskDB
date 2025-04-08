from langchain_google_genai import ChatGoogleGenerativeAI

from ai_chat_db.config import settings

model_list = [
    "gemini-2.5-pro-exp-03-25",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]


def main() -> None:
    """Main function to run the application."""
    # Example usage of the settings and model
    model = ChatGoogleGenerativeAI(
        model=model_list[1],
        google_api_key=settings.google_api_key,
    )
    question = "what is Python?"
    print(f"Question: {question}")
    print("Answer: ", end="")
    response = model.stream(question)
    for chunk in response:
        print(chunk.content, end="")
    print("\n")


if __name__ == "__main__":
    main()
