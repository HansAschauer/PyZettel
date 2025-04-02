import os
import pathlib
import platformdirs


from langchain_openai import OpenAIEmbeddings

# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from chromadb.config import Settings

from langchain_core.documents import Document
from langsmith import tracing_context
from pyzettel.zettel import Zettel

from .zettel_splitter import zettel_to_docs

import click
from pyzettel.cli.plugins import get_embedder_factory, RessourceNotFound

from .config import config#, get_embedder

import logging
logger = logging.getLogger(__name__)

@click.command()
@click.option("--llm-model", default=None, help="The model to use for the LLM")
@click.pass_context
def update(ctx: click.Context, llm_model: str | None):
    """
    Ask a question to the zettelkasten
    """
    os.environ.pop("LANGCHAIN_TRACING_V2", None)
    os.environ["LANGCHAIN_API_KEY"] = "xx"
    with tracing_context(enabled=False):
        cfg = ctx.obj.config

        chroma_data_dir = (
            pathlib.Path(
                config.get(
                    "chroma_data_dir", platformdirs.user_data_dir("pyzettel-ask")
                )
            )
            / "chroma_data"
        )
        try:
            embedding = get_embedder_factory()()
        except RessourceNotFound:
            logger.error(
                "No embedder found. Please enable a plugin that provides an embedder."
            )
            raise
        vectordb = Chroma(
            client_settings=Settings(anonymized_telemetry=False),
            persist_directory=str(chroma_data_dir), embedding_function=embedding
        )


        zettels = list(
            (pathlib.Path(cfg.zettelkasten_proj_dir) / cfg.zettelkasten_subdir).glob("0*.md")
        )
        # zettels = [Zettel.from_file(z) for z in zettels]

        docs: list[Document] = []
        ids: list[str] = []
        for z in zettels:
            zettel = Zettel.from_file(z)
            first_split = vectordb.get(ids=[f"{zettel.frontmatter.id}_0"])
            res = vectordb.get(where={"zettel_id": zettel.frontmatter.id})
            if first_split["metadatas"]:
                mtime = z.stat().st_mtime
                saved_meta = first_split["metadatas"][0]
                if saved_meta is not None and saved_meta["mtime"] < mtime:
                    vectordb.delete(res["ids"])
                    logger.info(
                        f"{z} is already in the vectorstore, but the file has been updated since the last time it was added to the vectorstore"
                    )
                else:
                    continue
            else:
                logger.debug(f"{z} is not in the vectorstore")
            splits, id_x = zettel_to_docs(z)
            logger.debug(f"Adding splits: {splits}")
            #texts = [s.page_content for s in splits]
            vectordb.add_documents(splits, ids=id_x)
            # vectordb.add_texts(texts, ids=id_x)
            splits, id_x = zettel_to_docs(z)
            docs.extend(splits)
            ids.extend(id_x)
        click.echo(f"zettels: {len(list(zettels))}")
        click.echo(f"document splits: {len(docs)}")




