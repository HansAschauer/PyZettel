from .conversation import Conversation
from pyzettel.config import Config
from .schema import Tags
from .prompts import generate_article, generate_tags


def generate_from_title(
    title: str,
    config: Config,
    language: str | None = None,
    existing_tags: list[str] = [],
    additional_input: str = "",
) -> tuple[str, dict[str, str]]:
    if config.ai_options is None:
        raise ValueError("AIOptions is required to use this function")
    conversation = Conversation(
        base_url=config.ai_options.base_url,
        api_key=config.ai_options.api_key,
        engine=config.ai_options.engine,
        developer_prompt="you are a helpful assistant, who provides only output when asked for it. Without any other text added.",
    )
    article = conversation.ask(
        generate_article(
            title=title, language=language, additional_input=additional_input
        )
    )
    tags_dict = conversation.ask_json(generate_tags(tags=existing_tags), model=Tags)
    return article, tags_dict
