import click
from ...zettel import Zettel
from ...config import load_config
from ...utils import filename_from_id
import subprocess
from rich.console import Console
from rich.markdown import Markdown


@click.command()
@click.argument(
    "id",
)
@click.option(
    "--show-title/--no-show-title",
    "-t/-T",
    default=True,
    help="Show title of zettel.",
)
@click.option(
    "--editor/--cli",
    "-e/-cli",
    default=False,
    help="Open zettel in editor.",
)
@click.option(
    "--show-filename/--no-show-filename",
    "-f/-F",
    default=False,
    is_flag=True,
    help="Show filename of zettel.",
)
def show(
    id: str, show_title: bool, editor: bool, show_filename: bool,
):
    "Show a zettel on the command line or in an editor."
    config = load_config(config_file)
    filename = filename_from_id(id, config)
    z = Zettel.from_file(filename)
    
    if show_title:
        click.echo(z.frontmatter.title)
    if show_filename:
        click.echo(filename)
    if editor:
        args = [config.editor] + config.editor_args + [filename]
        subprocess.Popen(args)
    else:
        console = Console()
        console.print(Markdown(z.content))
        
        
commands = [show]