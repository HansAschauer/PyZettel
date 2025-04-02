from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from typing import Union, Literal
# example config as YAML:
# api_name: "openai"
# api_key: "sk-xx"
# api_key_keyword: "api_key"
# additional_embedder_init_options:
#   base_url: "https://api.openai.com"
#   model: "text-davinci-003"
# chroma_data_dir: "/path/to/chroma_data"

# example for Google Generative AI:
# api_name: "google"
# api_key: "sk-xx"
# api_key_keyword: "google_api_key"
# additional_embedder_init_options:
#  model: "models/embedding-001"
# chroma_data_dir: "/path/to/chroma_data"
config = {}


embedding_name_to_class = {
    "openai": OpenAIEmbeddings,
    "google": GoogleGenerativeAIEmbeddings,
}

google_task_type_mapping: dict[str|None, str|None] = {
    "semantic_similarity": "semantic_similarity",
    "retrieval_document": "retrieval_document",
    "retrieval_query": "retrieval_query",
    "question_ansering": "question_answering",
    "fact_verification": "fact_verification",
    "classification": "classification",
    "clustering": "clustering",
    None: None,
}


# def get_embedder(
#     task_type: Literal[
#         "semantic_similarity",
#         "retrieval_document",
#         "retrieval_query",
#         "question_ansering",
#         "fact_verification",
#         "classification",
#         "clustering",
#         None
#     ],
# ) -> Union[OpenAIEmbeddings, GoogleGenerativeAIEmbeddings]:
#     kwargs = {}
#     if config["api_name"] == "google":
#         kwargs.update(
#             {
#                 "task_type": google_task_type_mapping[task_type],
#             }
#         )
#     kwargs.update({config["api_key_keyword"]: config["api_key"]})
#     kwargs.update(config.get("additional_embedder_init_options", {}))  # type: ignore
#     return embedding_name_to_class[config["api_name"]](**kwargs)
