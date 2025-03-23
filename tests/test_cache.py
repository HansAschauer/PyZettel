from pyzettel.cache import open_cache
from pathlib import Path

cach_dir = Path(__file__).parent / "cache"

def test_chache_simple():
    with open_cache("test_cache", cach_dir) as cache:
        cache["test_key"] = "test_value"
        assert cache["test_key"] == "test_value"
    
    with open_cache("test_cache", cach_dir) as cache:
        assert cache["test_key"] == "test_value"

