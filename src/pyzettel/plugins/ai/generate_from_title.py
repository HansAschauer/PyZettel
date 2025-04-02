from .conversation import Conversation
from pyzettel.config import Config
from .schema import Tags
from .prompts import generate_article, generate_tags
from ...cli.plugins import RessourceNotFound
import logging
logger = logging.getLogger(__name__)

def generate_from_title(
    title: str,
    config: Config,
    language: str | None = None,
    existing_tags: list[str] = [],
    additional_input: str = "",
) -> tuple[str, dict[str, str]]:
    try:
        conversation = Conversation(
            developer_prompt="you are a helpful assistant, who provides only output when asked for it. Without any other text added.",
        )
    except RessourceNotFound:
        raise ValueError("No LLM found. Please enable a plugin that provides an LLM.")
    article = conversation.ask(
        generate_article(
            title=title, language=language, additional_input=additional_input
        )
    )
    tags_dict = conversation.ask_json(generate_tags(tags=existing_tags), model=Tags)
    return article, tags_dict
