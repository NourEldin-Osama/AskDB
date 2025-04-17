from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

model = ChatGoogleGenerativeAI(
    model=settings.model_name,
    google_api_key=settings.GOOGLE_API_KEY,
)
