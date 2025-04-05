from langchain_core.embeddings.embeddings import Embeddings
from . import conf_module 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import Literal


def google_embedder(
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
    kwargs = {}
    if model := conf_module.config.get("embeddings_model"):
        kwargs["model"] = model
    return GoogleGenerativeAIEmbeddings(google_api_key=conf_module.config["api_key"], **kwargs,)
