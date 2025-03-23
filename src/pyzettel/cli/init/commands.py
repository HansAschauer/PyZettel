import click
import platformdirs
from click_loglevel import LogLevel

import pathlib

from ...config import Config, AIOptions

default_data_path = platformdirs.user_data_path("pyzettel")
cache_dir = platformdirs.user_cache_path("pyzettel")
default_config_path = platformdirs.user_config_path("pyzettel")

mkdocs_template = """
site_name: My Zettelkasten
theme:
  name: zettelkasten-solarized-light
plugins:
- tags
- zettelkasten"""


@click.command()
@click.option(
    "--config-file",
    "-c",
    default=default_config_path,
    help="Path to the configuration file",
)
@click.option(
    "--log-level", "-l", type=LogLevel(), default="INFO", help="Set logging level"
)
@click.option(
    "--zettelkasten-dir",
    "-z",
    help="Path to the zettelkasten directory",
    default=default_data_path,
)
@click.option(
    "--id-template",
    "-i",
    help="Template for generating zettel IDs",
    default="{{now | hexdate(12)}}",
)
@click.option(
    "--mkdocs/--no-mkdocs", "-m/-M", default=True, help="Generate mkdocs configuration"
)
@click.pass_context
def init(
    ctx: click.Context,
    config_file: str,
    zettelkasten_dir: str,
    id_template: str,
    mkdocs: bool,
):
    "Initialize a new pyzettel configuration"
    config_file_path = pathlib.Path(config_file)
    if pathlib.Path.exists(config_file_path):
        config = Config.from_yaml(config_file_path)

    else:
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        config = Config(zettelkasten_proj_dir=zettelkasten_dir, id_template=id_template)
        ai_options = AIOptions()
        config.ai_options = ai_options
        print(config)
        config_yaml = config.to_yaml()
        with open(config_file_path, "w") as f:
            f.write(config_yaml)
    click.echo(f"Initialized config file at {config_file_path}")
    click.echo(f"Zettelkasten directory is {config.zettelkasten_proj_dir}")
    click.echo(f"ID template is {config.id_template}")
    click.echo(f"Default data path is {default_data_path}")
    click.echo(f"Default config path is {config_file_path}")
    if not pathlib.Path.exists(default_data_path / "docs"):
        pathlib.Path.mkdir(default_data_path / "docs", parents=True, exist_ok=True)
        click.echo(f"Created default data path at {default_data_path}")

    if mkdocs:
        mkdirs_yml = default_data_path / "mkdocs.yml"
        if not mkdirs_yml.exists():
            with open(mkdirs_yml, "w") as f:
                f.write(mkdocs_template)
        else:
            click.echo("mkdocs.yml already exists. No action taken.")
            
    cache_path = pathlib.Path(cache_dir)
    cache_path.mkdir(exist_ok=True)

commands = [init]