import click
import platformdirs

import pathlib

from ...config import Config

default_data_path = platformdirs.user_data_path("pyzettel")
cache_dir = platformdirs.user_cache_path("pyzettel")
default_config_path = platformdirs.user_config_path("pyzettel")
plugins_config_file = platformdirs.user_config_path("pyzettel_plugins")

mkdocs_template = """
site_name: My Zettelkasten
theme:
  name: zettelkasten-solarized-light
plugins:
- tags
- zettelkasten
markdown_extensions:
- admonition
- meta
- codehilite:
- pymdownx.superfences

nav:
- start: index.md
"""

pyproject_template = """[project]
name = "zettelkasten"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "mkdocs-zettelkasten>=0.1.9",
    "mkdocs>=1.6.1",
]
"""

plugins_config_template = """
plugins:
  # uncomment to enable the AI plugin
  #pyzettel.plugins.ai:
  # uncomment to enable the hello plugin
  #pyzettel.plugins.hello:
  # uncomment to enable the rag (retrieval augmented generation) plugin
  #pyzettel.plugins.rag:
  #  api_name: "google"
  #  api_key: "google cloud api key"
  #  api_key_keyword: "google_api_key"
  #  additional_embedder_init_options:
  #    model: "models/embedding-001"    
loader_config:
  log_level: WARNING

"""

@click.command()
@click.option(
    "--config-file",
    "-c",
    default=default_config_path,
    help="Path to the configuration file",
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
@click.option(
    "--pyproject/--no-pyproject", "-p/-P", default=True, help="Generate pyproject.toml"
)

@click.pass_context
def init(
    ctx: click.Context,
    config_file: str,
    zettelkasten_dir: str,
    id_template: str,
    mkdocs: bool,
    pyproject: bool,
):
    "Initialize a new pyzettel configuration"
    config_file_path = pathlib.Path(config_file)
    if pathlib.Path.exists(config_file_path):
        config = Config.from_yaml(config_file_path)

    else:
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        config = Config(zettelkasten_proj_dir=zettelkasten_dir, id_template=id_template)
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
    if pyproject:
        pyproject_toml = default_data_path / "pyproject.toml"
        if not pyproject_toml.exists():
            with open(pyproject_toml, "w") as f:
                f.write(pyproject_template)
        else:
            click.echo("pyproject.toml already exists. No action taken.")
            
    if not plugins_config_file.exists():
        plugins_config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(plugins_config_file, "w") as f:
            f.write(plugins_config_template)
        click.echo(f"Created default plugins config file at {plugins_config_file}")
    else:
        click.echo(f"Plugins config file already exists at {plugins_config_file}")
    
            
    cache_path = pathlib.Path(cache_dir)
    cache_path.mkdir(exist_ok=True)

commands = [init]