from dataclasses import dataclass, field
import platformdirs
import pathlib
from .utils import YAMLSerializable
from .cli.plugins import PluginsConfig


@dataclass
class Config(YAMLSerializable):
    zettelkasten_proj_dir: str = platformdirs.user_data_dir("pyzettel")
    zettelkasten_subdir: str = "docs"
    id_template: str = "{{now | hexdate(12)}}"
    editor: str = "code"
    editor_args: list[str] = field(default_factory=list)
    #ai_options: AIOptions | None = None
    zettelkasten_paper_dir: str = ""
    bibtex_file: str = ""
    opencitations_api_key: str = ""


def load_config(config_file_name: str) -> "Config":
    config_file_path = pathlib.Path(config_file_name)
    if pathlib.Path.exists(config_file_path):
        config = Config.from_yaml(config_file_path)
    else:
        raise ValueError
    return config

def load_plugin_config(plugin_config_path: str | pathlib.Path) -> PluginsConfig:
    plugin_config_path = pathlib.Path(plugin_config_path)
    if pathlib.Path.exists(plugin_config_path):
        cfg = PluginsConfig.from_yaml(plugin_config_path)
        return cfg
    else:
        return PluginsConfig()