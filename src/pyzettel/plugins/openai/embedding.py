from langchain_core.embeddings.embeddings import Embeddings
from . import conf_module
from langchain_openai import OpenAIEmbeddings
from typing import Literal


def openai_embedder(
    task_type: Literal[
        "semantic_similarity",
        "retrieval_document",
        "retrieval_query",
        "question_ansering",
        "fact_verification",
        "classification",
        "clustering",
        None,
    ] = None,
) -> Embeddings:
    config = conf_module.config
    base_url = config.get("base_url")
    kwargs = {}
    if model := config.get("embeddings_model"):
        kwargs["model"] = model
    return OpenAIEmbeddings(api_key=config["api_key"], base_url=base_url, **kwargs)
