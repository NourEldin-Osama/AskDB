from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

model_list = [
    "gemini-2.5-pro-exp-03-25",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]

model_name = model_list[2]

model = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=settings.GOOGLE_API_KEY,
)
