from pyzettel.citations.zettel_from_doi import zettel_from_doi
from pyzettel.config import Config
import pathlib
config_file = pathlib.Path(__file__).parent / "pyzettel"
config = Config.from_yaml(yaml_file = config_file)

def test_zettel_from_doi():
    zettel = zettel_from_doi("10.1103/PHYSREVLETT.88.047902", config)
    assert zettel is not None
    print(zettel.render())
    
if __name__ == "__main__":
    test_zettel_from_doi()