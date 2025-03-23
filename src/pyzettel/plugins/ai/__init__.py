from . import config as conf_module
from .improve import improve
from .scrape import scrape
from .search import search
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

def set_config(conf: dict):
    conf_module.config = conf
    
config = conf_module.config

@click.group()
def ai():
    "AI commands group"
    pass

ai.add_command(improve)
ai.add_command(scrape)
ai.add_command(search)
ai.add_command(tags)
ai.add_command(create)

commands = [ai]