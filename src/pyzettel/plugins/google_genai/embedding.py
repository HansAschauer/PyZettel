from langchain_core.embeddings.embeddings import Embeddings
from .conf_module import config
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
) -> Embeddings: ...
