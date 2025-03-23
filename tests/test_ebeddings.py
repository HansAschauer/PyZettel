from pyzettel.zettel import Zettel, Frontmatter
from pyzettel.ai.embeddings import EmbeddingClient, cosine_similarity, embedding_avg
from pyzettel.config import Config

import numpy as np
from datetime import datetime
from pathlib import Path
config_file = Path(__file__).parent / "pyzettel"
config = Config.from_yaml(config_file)

def test_get_embedding() -> None:
    assert config.ai_options is not None
    print(config.ai_options)
    c = EmbeddingClient(config.ai_options.base_url, config.ai_options.api_key, config.ai_options.embeddings_engine, config.ai_options.embeddings_max_tokens)
    emb1 = c.get_embedding("Test")
    emb2 = c.get_embedding("das ist ein Test " * 500)
    
    print(f"{sum(emb1), sum(emb2), cosine_similarity(emb1, emb2)}")
    
def test_embeddings_avg():
    texts = ["Das ist ein Test", "Das ist ein Test", "Das ist ein"]
    embeddigns = [np.array([1, 2, 3]), np.array([1.1, 2.1, 3.1]), np.array([0.9, 1.9, 2.9])]
    lengths = [len(t) for t in texts]
    
    avg1 = embedding_avg(texts, embeddigns)
    avg2 = np.sum([embeddigns[i] * lengths[i] for i in range(len(texts))], axis=0) / sum(lengths)
    print(avg1, avg2)
    assert np.allclose(avg1, avg2)
    
    embeddigns = [np.array([1,2,3])]
    texts = ["Das ist ein Test"]
    avg1 = embedding_avg(texts, embeddigns)
    avg2 = embeddigns[0]
    print(avg1, avg2)
    assert np.allclose(avg1, avg2)
    
if __name__ == "__main__":
    test_embeddings_avg()