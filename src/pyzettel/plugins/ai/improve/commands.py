import click
from pyzettel.zettel import Zettel
from pyzettel.utils import filename_from_id
from ...ai.improve_document import improve_zettel
import subprocess


@click.command()
@click.option("--zettel-id", "-z", required=True, help="ID of the zettel")
@click.option(
    "--language", "-l", default=None, help="Language for the generated article"
)
@click.option(
    "--regards",
    "-r",
    multiple=True,
    help="Specify in which respects to improve. Can be given multiple times.",
)
@click.pass_context
def improve(
    ctx: click.Context,
    zettel_id: str,
    regards: list[str],
    language: str | None,
):
    "Improve an existing zettel using AI"
    config = ctx.obj.config
    zettel = Zettel.from_file(filename_from_id(zettel_id, config))
    new_content = improve_zettel(zettel.content, config, regards, language)
    
    zettel.content = f"""{zettel.content}

---
!!! note 
    The following is an AI generated *improvement* of the text above, using 
    the following improvement regards:
    
    - {"\n    - ".join(regards)}
{new_content}
"""
    
    zettel_file = filename_from_id(zettel.frontmatter.id, config)
    with open(zettel_file, "w") as f:
        f.write(zettel.render())
    click.echo(f"Created improved at {zettel_file}")

    args = [config.editor] + config.editor_args + [zettel_file]
    subprocess.Popen(args)

commands = [improve]