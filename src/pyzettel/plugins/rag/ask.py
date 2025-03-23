from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_openai.chat_models import ChatOpenAI

from langchain_core.utils.utils import convert_to_secret_str
import pathlib
import pyzettel.config
import platformdirs

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langsmith import tracing_context
from langchain_core.prompts.chat import ChatPromptTemplate

from typing import Literal
from dataclasses import dataclass, field

import os

import click
from .config import config, get_embedder

from rich.console import Console
from rich.markdown import Markdown
import logging
logger = logging.getLogger(__name__)

def where_filter(zettel_id: str, doc_type: Literal["tag", "split"]) -> dict:
    return {"$and": [{"zettel_id": zettel_id}, {"type": doc_type}]}


my_prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are question-answering bot in a RAG pipeline. Answer the question using "
            "the retrieved context.  If you don't know the answer, just say that you don't "
            "know. Use one to five paragraphs maximum and keep the answer concise. The answer "
            "MUST be formatted in Markdown. You may"
            "Add code snippets when it is helpful. Start like this:\n"
            "# Question\n\n<question>\n\n# Answer\n\n<answer>",
        ),
        ("human", "Question: {question}\n\nContext: {context}\n\nAnswer:"),
    ]
)


@dataclass
class DocumentFormatter:
    vectordb: Chroma
    zettels: set[tuple[str, str]] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)

    def clear(self):
        self.zettels.clear()
        self.tags.clear()

    def format_docs(self, docs: list[Document]) -> str:
        page_contents = []
        for d in docs:
            if "type" not in d.metadata:
                print("no type found, continuing")
                print(d)
                continue
            if d.metadata["type"] == "tag":
                self.tags.add(d.page_content)
                res1 = self.vectordb.get(
                    where=where_filter(d.metadata["zettel_id"], "split")
                )
                zettels = {(m["zettel_id"], m["title"]) for m in res1["metadatas"]}
                self.zettels.update(zettels)
                page_contents.extend(res1["documents"])
            else:
                page_contents.append(d.page_content)
                self.zettels.add((d.metadata["zettel_id"], d.metadata["title"]))
        return "\n\n".join(page_contents)


@click.command()
@click.option("--llm-model", default=None, help="The model to use for the LLM")
@click.option("--show-used-zettels/--no-show-used-zettels", "-z/-Z", default=False)
@click.option("--show-used-tags/--no-show-used-tags", "-t/-T", default=False)
@click.option("--markdown/--no-markdown", "-m/-M", default=True)
@click.argument("question")
def ask(
    llm_model: str | None,
    question: str,
    show_used_zettels: bool,
    show_used_tags: bool,
    markdown: bool,
):
    """
    Ask your zettelkasten a question.
    """
    os.environ.pop("LANGCHAIN_TRACING_V2", None)
    os.environ["LANGCHAIN_API_KEY"] = "xx"
    with tracing_context(enabled=False):
        cfg = pyzettel.config.load_config(platformdirs.user_config_dir("pyzettel"))
        ai_cfg = cfg.ai_options
        assert ai_cfg is not None
        api_key = convert_to_secret_str(ai_cfg.api_key)

        chroma_data_dir = (
            pathlib.Path(
                config.get(
                    "chroma_data_dir", platformdirs.user_data_dir("pyzettel-ask")
                )
            )
            / "chroma_data"
        )
        if llm_model is None:
            llm_model = config.get("llm_model", ai_cfg.engine)
            assert isinstance(llm_model, str)

        base_url = ai_cfg.base_url

        #embedding = OpenAIEmbeddings(
        #    api_key=api_key, base_url=base_url, model=ai_cfg.embeddings_engine
        #)
        embedding = get_embedder("retrieval_query")

        vectordb = Chroma(
            client_settings=Settings(anonymized_telemetry=False),
            persist_directory=str(chroma_data_dir), embedding_function=embedding
        )

        # https://python.langchain.com/docs/versions/migrating_chains/retrieval_qa/
        # llm = ChatOpenAI(api_key=api_key, base_url=base_url, model="mistral-nemo-instruct-2407")
        llm = ChatOpenAI(api_key=api_key, base_url=base_url, model=llm_model)

        formatter = DocumentFormatter(vectordb)
        qa_chain = (
            {
                "context": vectordb.as_retriever() | formatter.format_docs,
                "question": RunnablePassthrough(),
            }
            | my_prompt
            | llm
            | StrOutputParser()
        )

        formatter.clear()

        answer = qa_chain.invoke(question)
        if show_used_zettels:
            click.echo("Zettels used:")
            for zettel_id, title in formatter.zettels:
                click.echo(f"{zettel_id}: {title}")
            click.echo("---------------------------------------")
        if show_used_tags:
            click.echo("Tags used:")
            click.echo("- " + "- \n".join(formatter.tags))
            click.echo("---------------------------------------")
        if markdown:
            logger.debug("markdown output selected")
            console = Console()
            console.print(Markdown(answer))
        else:
            click.echo(answer)
        