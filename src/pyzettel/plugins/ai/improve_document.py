from .conversation import Conversation
from pyzettel.config import Config
from .prompts import generate_improve_zettel
from ...cli.plugins import RessourceNotFound


def improve_zettel(
    document: str,
    config: Config,
    improve_regards: list[str],
    language: str | None,
) -> str:
    try:
        conversation = Conversation(
            developer_prompt="you are a helpful assistant, who provides only output when asked for it. Without any other text added.",
        )
    except RessourceNotFound:
        raise ValueError("No LLM found. Please enable a plugin that provides an LLM.")
    article = conversation.ask(
        generate_improve_zettel(
            document, improve_regards, language=language, 
        )
    )
    return article
