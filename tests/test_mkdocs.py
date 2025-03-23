from pyzettel.mkdocs.tags import get_tags
from pathlib import Path
from pyzettel.config import Config

config_file = Path(__file__).parent / "pyzettel"
config = Config.from_yaml(config_file)

def test_get_tags():
    tags = get_tags(config)
    print(tags)
    
    
if __name__ == "__main__":
    test_get_tags()