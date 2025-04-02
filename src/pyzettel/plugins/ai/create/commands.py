import datetime
import click
from pyzettel.zettel import Zettel, Frontmatter
from pyzettel.utils import filename_from_id
from pyzettel.mkdocs.tags import get_tags
from ..generate_from_title import generate_from_title
import subprocess


@click.command()
@click.option("--title", "-t", required=True, help="Title of the zettel")
@click.option("--tag", "-g", multiple=True, help="Tags for the zettel")
@click.option(
    "--language", "-l", default=None, help="Language for the generated article"
)
@click.option("--additional-input", "-i", default="", help="Additional input for AI")
@click.pass_context
def create(
    ctx: click.Context,
    title: str,
    tag: list[str],
    language: str | None,
    additional_input: str,
):
    "Create a new zettel"
    config = ctx.obj.config
    tag = list(tag)
    content = f"# {title}\n"
    if language is None:
        language = config.language
    existing_tags = get_tags(config)
    article, tags = generate_from_title(
        title,
        config,
        language,
        existing_tags=existing_tags,
        additional_input=additional_input,
    )
    content = article
    ai_tags = tags["tags"]
    tag = list(set(tag) | set(ai_tags))
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