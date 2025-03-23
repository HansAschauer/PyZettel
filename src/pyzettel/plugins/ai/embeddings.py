import numpy as np
from openai import OpenAI
from dataclasses import dataclass, field
from base64 import b64encode, b64decode
from more_itertools import chunked

# Some methods take ideas from openai-cookbook:
# https://github.com/openai/openai-cookbook/blob/main/examples/utils/embeddings_utils.py
# and from the pyhton cookbook
@dataclass
class EmbeddingClient:
    base_url: str
    api_key: str
    engine: str
    embeddings_max_tokens: int

    client: OpenAI = field(init=False)
    
    def __post_init__(self):
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_embeddings(
        self, list_of_text: list[str], **kwargs
    ) -> list[np.ndarray]:
        assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."

        # replace newlines, which can negatively affect performance.
        list_of_text = [text.replace("\n", " ") for text in list_of_text]

        data = self.client.embeddings.create(input=list_of_text, model=self.engine, **kwargs).data
        return [np.array(d.embedding, dtype=np.float32) for d in data]


    def get_embedding(self, text: str, **kwargs) -> np.ndarray:
        chunks = chunked_string(text, self.embeddings_max_tokens)
        embeddings = self.get_embeddings(chunks,  **kwargs)
        return embedding_avg(chunks, embeddings)
        

def embedding_avg(
    texts: list[str], embeddings: list[np.ndarray]
) -> np.ndarray:
    texts = ["".join(t) for t in texts]
    lengths = np.array([len(t) for t in texts])
    lengths = lengths / sum(lengths)
    embeddings_a =  np.array(embeddings)  
    return np.matmul(embeddings_a.T, lengths)

def chunked_string(text: str, n: int) -> list[str]:
    chunks = chunked(text, n)
    return ["".join(c) for c in chunks] 

def similarity_matrix(embeddings: list[np.ndarray]) -> np.ndarray:
    num_embeddings = len(embeddings)
    # res = np.array([[cosine_similarity(a, b) for b in embeddings] for a in embeddings])
    
    e = np.array(embeddings)
    e_norm = e / np.linalg.norm(e, axis=1).reshape(num_embeddings, 1)
    res = np.matmul(e_norm, e_norm.T)
    
    return res
        

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def embedding_to_string(embedding: np.ndarray) -> str:
    embedding = embedding.astype(np.float32)
    return b64encode(embedding.tobytes()).decode("utf-8")

def embedding_from_string(embedding_str: str) -> np.ndarray:
    embedding = np.frombuffer(b64decode(embedding_str), dtype=np.float32)
    return embedding



# def batched(text: str, n) -> Iterable[Iterable[str]]:
#     """Batch data into tuples of length n. The last batch may be shorter."""
#     # batched('ABCDEFG', 3) --> ABC DEF G
#     if n < 1:
#         raise ValueError('n must be at least one')
#     it = iter(text)
#     ii = islice(it, 3)
#     x = next(ii)
#     while (batch := tuple(islice(it, n))):
#         yield batch
