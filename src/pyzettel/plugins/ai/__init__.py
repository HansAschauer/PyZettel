from . import config as conf_module
from .improve import improve
from .scrape import scrape
from .search import search, index
from .tags import tags
from .create import create

from pyzettel.cli.plugins import PluginMissingDependencies
import click

try:
    import openai  # noqa: F401
    import numpy  # noqa: F401
    import bs4  # noqa: F401
except ImportError as e:
    raise PluginMissingDependencies(
        f"Missing dependencies for plugin. Disable plugin to get rid of this warning: {e}"
    ) from e

    
config = conf_module.config

@click.group()
def ai():
    "AI commands group"
    pass

ai.add_command(improve)
ai.add_command(scrape)
ai.add_command(search)
ai.add_command(index)
ai.add_command(tags)
ai.add_command(create)

# Plugin interface as defined in pyzettel.cli.plugins.PluginModule

def set_config(conf: dict):
    conf_module.config = conf

commands = [ai]

embedder_factory = None
llm_factory = None
vector_store_factory = None

hooks = {}