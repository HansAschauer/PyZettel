import os
import pathlib
import platformdirs



# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from chromadb.config import Settings

from langchain_core.utils.utils import convert_to_secret_str
from langchain_core.documents import Document
from langsmith import tracing_context
import pyzettel.config

from .zettel_splitter import zettel_to_docs
from .config import config, get_embedder
import click


@click.command()
def init_db():
    "Initialialize database used for RAG."
    os.environ["LANGCHAIN_API_KEY"] = "xx"
    
    with tracing_context(enabled=False):
        cfg = pyzettel.config.load_config(platformdirs.user_config_dir("pyzettel"))
        ai_cfg = cfg.ai_options
        assert ai_cfg is not None

        chroma_data_dir = (
            pathlib.Path(
                config.get("chroma_data_dir", platformdirs.user_data_dir("pyzettel-ask"))
            )
            / "chroma_data"
        )
        chroma_data_dir.mkdir(parents=True, exist_ok=True)

        api_key = convert_to_secret_str(ai_cfg.api_key)
        os.environ["LANGSMITH_TRACING"] = "false"
        base_url = ai_cfg.base_url

        zettels = list(
            (pathlib.Path(cfg.zettelkasten_proj_dir) / cfg.zettelkasten_subdir).glob(
                "*.md"
            )
        )

        docs: list[Document] = []
        ids: list[str] = []
        for z in zettels:
            splits, id_x = zettel_to_docs(z)
            docs.extend(splits)
            ids.extend(id_x)
        print("zettels:", len(list(zettels)))
        print("document splits:", len(docs))

#        embedding = OpenAIEmbeddings(
#            api_key=api_key, base_url=base_url, model=ai_cfg.embeddings_engine
#        )
        embedding = get_embedder("retrieval_document")
        _ = Chroma.from_documents(
            documents=docs,
            client_settings=Settings(anonymized_telemetry=False),
            ids=ids,
            embedding=embedding,
            persist_directory=str(chroma_data_dir),
        )
