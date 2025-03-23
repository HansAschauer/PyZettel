from pyzettel.cli.search.models import ZettelIndexEntry, ZettelIndex
from pyzettel.config import Config
from pyzettel.zettel import Zettel
from pyzettel.ai.embeddings import EmbeddingClient, embedding_from_string, cosine_similarity
from pathlib import Path

local_dir = Path(__file__).parent
config = Config.from_yaml(local_dir/"pyzettel")
assert config.ai_options is not None
ai_options = config.ai_options
client = EmbeddingClient(
    ai_options.base_url, 
    ai_options.api_key, 
    ai_options.embeddings_engine, 
    ai_options.embeddings_max_tokens
)


def test_zettel_index_entry():
    zettel = Zettel.from_file(local_dir / "assets" / "019543577ce8.md")
    zie = ZettelIndexEntry.from_zettel(zettel, config, client)
    print(zie)
    embedding_search1 = client.get_embedding("Brotbacken, Sauerteig, ohne Zusatzstoffe")
    embedding_search2 = client.get_embedding("Kuchenbacken, Backpulver")
    embedding_zettel = embedding_from_string(zie.embedding_title)
    print(cosine_similarity(embedding_search1, embedding_zettel))
    print(cosine_similarity(embedding_search2, embedding_zettel))
    
    
if __name__ == '__main__':
    test_zettel_index_entry()