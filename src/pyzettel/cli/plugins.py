from typing import Protocol, Iterable, Any
import click
from importlib import import_module
import logging

logger = logging.getLogger(__name__)

class PluginMissingDependencies(Exception):
    pass

class PluginModule(Protocol):
    @staticmethod
    def set_config(conf: dict[str, Any]): ...

    commands: Iterable[click.Command]


def register_plugins(
    plugin_config: dict[str, Any],
    main_group: click.Group,
):
    for plugin_name, plugin_config in plugin_config.items():
        try:
            logger.info(f"Loading plugin {plugin_name}")
            plugin_module: PluginModule = import_module(f"{plugin_name}") # type: ignore
            plugin_module.set_config(plugin_config)
            for command in plugin_module.commands:
                main_group.add_command(command)
        except ImportError as e:
            logger.warning(f"Failed to load plugin {plugin_name}")
            logger.exception(e)
            continue
        except AttributeError:
            logger.error(f"Plugin {plugin_name} does not have required attributes")
            continue
        except PluginMissingDependencies as e:
            logger.warning(f"Plugin {plugin_name} is missing dependencies: {e}")
            continue
        except Exception as e:
            logger.warning(f"Error loading plugin {plugin_name}: {e}")
            continue
