from . import conf_module
from .embedding import openai_embedder
from .llm import openai_llm


# Plugin interface as defined in pyzettel.cli.plugins.PluginModule
def set_config(conf: dict):
    conf_module.config = conf
   
commands = []
embedder_factory = openai_embedder
llm_factory = openai_llm
vector_store_factory = None

hooks = {}