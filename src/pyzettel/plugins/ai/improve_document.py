from .conversation import Conversation
from pyzettel.config import Config
from .prompts import generate_improve_zettel


def improve_zettel(
    document: str,
    config: Config,
    improve_regards: list[str],
    language: str | None,
) -> str:
    if config.ai_options is None:
        raise ValueError("AIOptions is required to use this function")
    conversation = Conversation(
        base_url=config.ai_options.base_url,
        api_key=config.ai_options.api_key,
        engine=config.ai_options.engine,
        developer_prompt="you are a helpful assistant, who provides only output when asked for it. Without any other text added.",
    )
    article = conversation.ask(
        generate_improve_zettel(
            document, improve_regards, language=language, 
        )
    )
    return article
