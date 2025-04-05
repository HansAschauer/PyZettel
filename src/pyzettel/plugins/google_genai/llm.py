from langchain_core.language_models.chat_models import BaseChatModel
from . import conf_module
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

def google_llm() -> BaseChatModel:
    config = conf_module.config
    kwargs = {}
    if model := config.get("llm_model"):
        kwargs["model"] = model
    return ChatGoogleGenerativeAI(api_key=config["api_key"],
                                  **kwargs)