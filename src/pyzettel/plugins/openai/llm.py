from langchain_core.language_models.chat_models import BaseChatModel
from . import conf_module
from langchain_openai.chat_models import ChatOpenAI


def openai_llm() -> BaseChatModel:
    config = conf_module.config
    base_url = config.get("base_url")
    kwargs = {}
    if model := config.get("llm_model"):
        kwargs["model"] = model
    return ChatOpenAI(api_key=config["api_key"],
                      base_url = base_url,
                      **kwargs)