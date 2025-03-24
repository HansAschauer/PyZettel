import click
from ...zettel import Zettel
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
@click.pass_context
def rm(ctx: click.Context, id: str, force: bool):
    "Delete a zettel"
    config = ctx.obj.config
    filename = filename_from_id(id, config)
    z = Zettel.from_file(filename)

    if not force:
        click.confirm(f"Delete {id}, '{z.frontmatter.title}'?", abort=True)
    Path(filename).unlink()


commands = [rm]
