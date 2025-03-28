from langchain_core.language_models.chat_models import BaseChatModel
from .conf_module import config
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

def google_llm() -> BaseChatModel:
    ...