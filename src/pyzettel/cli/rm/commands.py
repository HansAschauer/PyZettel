import click
from ...zettel import Zettel
from ..common_options import common_options
from ...config import load_config
from ...utils import filename_from_id
from pathlib import Path

@click.command()
@click.argument(
    "id",
)
@click.option(
    "--force/--no-force",
    "-f/-F",
    default=False,
    is_flag=True,
    help="Force deletion without confirmation.",
)
@common_options
def rm(id: str, force: bool, config_file: str):
    "Delete a zettel"
    config = load_config(config_file)
    filename = filename_from_id(id, config)
    z = Zettel.from_file(filename)

    if not force:
        click.confirm(f"Delete {id}, '{z.frontmatter.title}'?", abort=True)
    Path(filename).unlink()

commands = [rm]