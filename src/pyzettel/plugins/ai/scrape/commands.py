from ...ai.web_scraper import zettel_from_url
from pyzettel.mkdocs.tags import get_tags
import click

import subprocess


@click.command()
@click.argument("url", type=str)
#@click.option("--url", "-u", default=None, help="URL of web page to scrape")
@click.option("--file", "-f", default=None, help="File containing HTML to scrape")
@click.option(
    "--tag",
    "-g",
    multiple=True,
    help="Tags for the zettel. Will be added to the auto generated tags.",
)
@click.pass_context
def scrape(
    ctx: click.Context,
    url: str | None,
    file: str | None,
    tag: list[str],
):
    "Scrape a web page at URL."
    config = ctx.obj.config
    tags = set(tag)
    existing_tags = get_tags(config)
    z = zettel_from_url(url, config, from_file=file, existing_tags=existing_tags)
    z.frontmatter.tags = list(tags | set(z.frontmatter.tags))

    zettel_file = z.write_to_zettelfile(config)
    click.echo(f"Created zettel at {zettel_file}")

    args = [config.editor] + config.editor_args + [zettel_file]
    subprocess.Popen(args)

commands = [scrape]