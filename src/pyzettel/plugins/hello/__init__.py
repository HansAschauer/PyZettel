from .commands import commands, set_config  # noqa: F401

# Plugin interface as defined in pyzettel.cli.plugins.PluginModule
# commands and set_config is imported from commands.py
hooks = {}

embedder_factory = None
llm_factory = None
vector_store_factory = None

