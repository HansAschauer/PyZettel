from typing import Protocol, Iterable, Any, TypeAlias, Literal, Callable, Type
import click
from importlib import import_module
from dataclasses import dataclass, field
from ..utils import YAMLSerializable
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStore

import logging
logger = logging.getLogger(__name__)


ResourceTypes: TypeAlias = Literal["embedder", "llm", "vector_store"]
HookTypes: TypeAlias = Literal["create_zettel", "modify_zettel", "delete_zettel"]

class RessourceNotFound(ValueError):
    pass


class HasPriorityAndPluginName(Protocol):
    priority: int
    plugin_name: str
    
@dataclass
class EmbedderDeclaration:
    embedder_type: Type[Embeddings]
    priority: int
    plugin_name: str

@dataclass
class LLMDeclaration:
    llm_type: Type[BaseChatModel]
    priority: int
    plugin_name: str

@dataclass
class VectorStoreDeclaration:
    vector_store_type: type[VectorStore]
    priority: int
    plugin_name: str


@dataclass 
class Hook:
    plugin_name: str
    hook_function: Callable
    
vector_store_factories: list[VectorStoreDeclaration] = []
llm_factories: list[LLMDeclaration] = []
embedder_factories: list[EmbedderDeclaration] = []

hooks: dict[HookTypes, list[Hook]] = {
    "create_zettel": [], 
    "modify_zettel": [], 
    "delete_zettel": []
}

@dataclass
class PluginConfig(YAMLSerializable):
    enabled: bool = True
    resource_priorities: dict[ResourceTypes, int] = field(default_factory=dict)
    options: dict[str, Any] = field(default_factory=dict)

@dataclass
class LoaderConfig:
    log_level: str = "WARNING"


@dataclass
class PluginsConfig(YAMLSerializable):
    plugins: dict[str, PluginConfig] = field(default_factory=dict)
    loader_config: LoaderConfig = field(default_factory=LoaderConfig)


class PluginMissingDependencies(Exception):
    pass


class PluginModule(Protocol):
    @staticmethod
    def set_config(conf: dict[str, Any]): ...

    commands: Iterable[click.Command]
    #resource_factories: Mapping[ResourceTypes, Callable]
    embedder_factory: type[Embeddings] |None
    llm_factory: type[BaseChatModel] | None
    vector_store_factory: type[VectorStore] | None
    hooks: dict[HookTypes, Callable] = field(default_factory=dict)


def register_plugins(
    plugins_config: dict[str, PluginConfig],
    main_group: click.Group,
):
    for plugin_name, plugin_config in plugins_config.items():
        logger.info(f"plugin {plugin_name}")
        if not plugin_config.enabled:
            logger.debug("...plugin disabled.")
            continue
        try:
            logger.info(f"Loading plugin {plugin_name}")
            logger.debug(f"Plugin config: {plugin_config}")
            plugin_module: PluginModule = import_module(f"{plugin_name}")  # type: ignore
            plugin_module.set_config(plugin_config.options)
            # set CLI commands
            for command in plugin_module.commands:
                main_group.add_command(command)
            # set resource factories
            if plugin_module.embedder_factory:
                embedder_factories.append(EmbedderDeclaration(plugin_module.embedder_factory, plugin_config.resource_priorities.get("embedder", 10), plugin_name))
            if plugin_module.llm_factory:
                llm_factories.append(LLMDeclaration(plugin_module.llm_factory, plugin_config.resource_priorities.get("llm", 10), plugin_name))
            if plugin_module.vector_store_factory:
                vector_store_factories.append(VectorStoreDeclaration(plugin_module.vector_store_factory, plugin_config.resource_priorities.get("vector_store", 10), plugin_name))
            # set hooks:
            for hook_type, hook_function in plugin_module.hooks.items():
                hooks[hook_type].append(Hook(plugin_name, hook_function))
        except ImportError as e:
            logger.warning(f"Failed to load plugin {plugin_name}")
            logger.exception(e)
            continue
        except AttributeError as e:
            logger.error(f"Plugin {plugin_name} does not have required attributes")
            logger.debug("Exception:", exc_info=e)
            continue
        except PluginMissingDependencies as e:
            logger.warning(f"Plugin {plugin_name} is missing dependencies: {e}")
            continue
        except Exception as e:
            logger.warning(f"Error loading plugin {plugin_name}: {e}")
            continue



def get_embedder_factory() -> Type[Embeddings]:
    try: 
        f_list = [(f.priority, f.embedder_type) for f in embedder_factories]
        f_list.sort()
        factory = f_list[-1][1]
    except IndexError:
        raise RessourceNotFound("No Embedder found. Enable a plugin that provides an embedder.")
    return factory

def get_llm_factory() -> Type[BaseChatModel]:
    try: 
        f_list = [(f.priority, f.llm_type) for f in llm_factories]
        f_list.sort()
        factory = f_list[-1][1]
    except IndexError:
        raise RessourceNotFound("No LLM found. Enable a plugin that provides an LLM.")
    return factory

def get_vector_store_factory() -> Type[VectorStore]:
    try: 
        f_list = [(f.priority, f.vector_store_type) for f in vector_store_factories]
        f_list.sort()
        factory = f_list[-1][1]
    except IndexError:
        raise RessourceNotFound("No Vector Store found. Enable a plugin that provides a vector store.")
    return factory