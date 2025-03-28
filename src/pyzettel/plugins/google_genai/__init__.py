from . import conf_module
from .embedding import google_embedder
from .llm import google_llm

# Plugin interface as defined in pyzettel.cli.plugins.PluginModule
def set_config(conf: dict):
    conf_module.config = conf
   
commands = []
resource_factoies = {
    "embedder": google_embedder,
    "llm": google_llm,
}
embedder_factory = google_embedder
llm_factory = google_llm
hooks = {}