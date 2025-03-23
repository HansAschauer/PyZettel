from . import config as conf_module
from .init_db import init_db
from .ask import ask
from .update import update
from pyzettel.cli.plugins import PluginMissingDependencies
import os
import click

try:
    import chromadb  # noqa: F401
    import langchain_core  # noqa: F401
    import langchain_chroma  # noqa: F401
    import langsmith  # noqa: F401
except ImportError as e:
    raise PluginMissingDependencies(
        "Missing dependencies for plugin. Disable plugin to get rid of this warning."
    ) from e


os.environ["LANGSMITH_TRACING_V2"] = "false"


def set_config(conf: dict):
    conf_module.config = conf


config = conf_module.config


@click.group()
def rag():
    "Retrieval augmented generation commands group"
    pass


rag.add_command(init_db)
rag.add_command(ask)
rag.add_command(update)
commands = [rag]
