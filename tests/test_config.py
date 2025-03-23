from pyzettel.config import Config
import platformdirs


def test_config():
    config = Config()
    assert config.zettelkasten_proj_dir == platformdirs.user_data_dir("pyzettel")
    assert config.id_template == "{{now | hexdate(12)}}"
    config = Config(zettelkasten_proj_dir="test", id_template="{{now | intdate(14)}}")
    assert config.zettelkasten_proj_dir == "test"
    assert config.id_template == "{{now | intdate(14)}}"