from .conversation import Conversation
from pyzettel.zettel import Zettel, Frontmatter
from pyzettel.config import Config
from .schema import Tags
from .prompts import generate_tags
from bs4 import BeautifulSoup
import requests
import pathlib

footer = "[{url}]({url})"


def zettel_from_url(
    url: str | None,
    config: Config,
    from_file: str | pathlib.Path | None = None,
    existing_tags: list[str] | None = None,
) -> Zettel:
    if existing_tags is None:
        existing_tags = []
    if config.ai_options is None:
        raise ValueError("AIOptions is required to use this function")
    if url is not None:
        page_content = requests.get(url).content
    elif from_file is not None:
        page_content = open(from_file).read()
    else:
        raise ValueError("One of 'url' or 'from_file' must be given.")

    soup = BeautifulSoup(page_content, "html.parser")
    conversation = Conversation(
        base_url=config.ai_options.base_url,
        api_key=config.ai_options.api_key,
        engine=config.ai_options.engine,
        developer_prompt="you are a helpful assistant, who provides only output when asked for it. Without any other text added.",
    )
    _ = conversation.ask(
        "In the following task, consider the text between <begin> and <end> as the input text."
        + f"<begin>{soup.get_text()}<end>. Do not output anything."
    )
    tags = conversation.ask_json(generate_tags(existing_tags), model=Tags)
    print("xxx tags", tags)
    title = conversation.ask("Output a title of the text")
    author = conversation.ask("""Output the author of the text, if you find reliable data. 
                              Otherwise, output 'None'""")
    author = conversation.ask(f"""Please make sure that your previous answer, 
                              '{author}', 
                              actually represents a valid author name. It could also 
                              contain an affiliation, or the name of a 
                              company name which employs the author. Please reply 
                              the author name (in the format 'Firstname Lastname') or 
                              'None', without any other text.""")
    summary = conversation.ask("Output a summary of the text")

    content = f"# {title}\n\n{summary}"

    tag_list = tags["tags"]

    frontmatter = Frontmatter(
        title=title,
        tags=tag_list,
        _id_template=config.id_template,
    )
    frontmatter._additional_attributes["ai_generated"] = True
    if author.lower() != "none":
        frontmatter._additional_attributes["author"] = author

    return Zettel(
        frontmatter=frontmatter, content=content, footer=footer.format(url=url)
    )
