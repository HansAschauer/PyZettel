import click
import platformdirs
from click_loglevel import LogLevel
from dataclasses import dataclass
from pathlib import Path
import os
from ..config import load_config, Config, load_plugin_config
from .plugins import register_plugins
from importlib import import_module
import logging

logger = logging.getLogger(__name__)

default_config_path = platformdirs.user_config_path("pyzettel")
default_plugin_config_path = platformdirs.user_config_path("pyzettel_plugins")
plugin_config_path = os.environ.get(
    "PYZETTEL_PLUGIN_CONFIG", default_plugin_config_path
)


@dataclass
class CLIContext:
    config: Config | None = None


@click.group()
@click.option(
    "--config-file",
    "-c",
    default=default_config_path,
    help="Path to the configuration file",
)
@click.option(
    "--log-level", "-l", type=LogLevel(), default="WARNING", help="Set logging level"
)
@click.pass_context
def entry_point(ctx: click.Context, config_file: str, log_level: int):
    logging.basicConfig(level=log_level)
    try:
        config = load_config(config_file)
    except ValueError:
        return
    ctx.ensure_object(CLIContext)
    ctx.obj.config = config


#@entry_point.group()
#@click.pass_context
#def plugin(ctx: click.Context):
#    pass


cli_modules = Path(__file__).parent.glob("*/__init__.py")
for module in cli_modules:
    module_name = module.parent.name
    logger.debug(f"Importing module {module_name}")
    module = import_module(f".{module_name}", __package__)
    for command in module.commands:
        entry_point.add_command(command)

plugin_config = load_plugin_config(plugin_config_path)
logging.basicConfig(
    level=plugin_config.get("loader_config", dict()).get("log_level", "WARNING")
)
register_plugins(plugin_config.get("plugins", dict()), entry_point)
