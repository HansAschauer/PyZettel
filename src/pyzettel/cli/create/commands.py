import datetime
import click
from ...zettel import Zettel, Frontmatter
from ...utils import filename_from_id
import subprocess


@click.command()
@click.option("--title", "-t", required=True, help="Title of the zettel")
@click.option("--tag", "-g", multiple=True, help="Tags for the zettel")

@click.pass_context
def create(
    ctx: click.Context,
    title: str,
    tag: list[str],
):
    "Create a new zettel"
    config = ctx.obj.config
    tag = list(tag)
    content = f"# {title}\n"
    z = Zettel(
        frontmatter=Frontmatter(
            title=title,
            date=datetime.datetime.now(),
            _id_template=config.id_template,
            tags=tag,
        ),
        content=content,
    )

    zettel_file = filename_from_id(z.frontmatter.id, config)
    with open(zettel_file, "w") as f:
        f.write(z.render())
    click.echo(f"Created zettel at {zettel_file}")

    args = [config.editor] + config.editor_args + [zettel_file]
    subprocess.Popen(args)

commands = [create]