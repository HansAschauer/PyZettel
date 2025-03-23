import click
from click_loglevel import LogLevel
import logging
import platformdirs

from .init_db import init_db
from .ask import ask
from .update import update

from pyzettel.cli.cli import CLIContext
from pyzettel.config import load_config

default_config_path = platformdirs.user_config_path("pyzettel")

@click.group()
@click.option(
    "--config-file",
    "-c",
    default=default_config_path,
    help="Path to the configuration file",
)
@click.option(
    "--log-level", "-l",
    type=LogLevel(),
    default="INFO",
    help="Set logging level")
@click.pass_context
def cli(ctx: click.Context, log_level: int, config_file: str):
    logging.basicConfig(level=log_level)
    try:
        config = load_config(config_file)
    except ValueError:
        return
    ctx.ensure_object(CLIContext)
    ctx.obj.config = config

cli.add_command(init_db)
cli.add_command(ask)
cli.add_command(update)