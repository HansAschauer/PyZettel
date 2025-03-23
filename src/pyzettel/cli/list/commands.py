import yaml
import click
from ...zettel import Zettel

import pathlib
from typing import Iterable
from logging import getLogger

logger = getLogger(__name__)


@click.command()
@click.argument("glob", default="*")
@click.option(
    "--show-tags",
    "-a",
    is_flag=True,
    help="display tags for listed zettels.",
)
@click.option(
    "--show-titles",
    "-t",
    is_flag=True,
    help="show titles of listed zettels.",
)
@click.pass_context
def list(
    ctx: click.Context,
    glob: str,
    show_tags: bool,
    show_titles: bool,
):
    "List zettels, using GLOB as a search pattern. GLOB defaults to '*'"
    config = ctx.obj.config

    path_glob = pathlib.Path(config.zettelkasten_proj_dir) / "docs"
    logger.debug(f"Zettel directory: {path_glob}")
    results = []
    for f in path_glob.glob("*.md"):
        try:
            z = Zettel.from_file(f)
            f_name = pathlib.Path(f).name
            res_struct: dict[str, str | Iterable] = dict(filename=f_name)

            if show_titles:
                res_struct["title"] = z.frontmatter.title
            if show_tags:
                res_struct["tags"] = z.frontmatter.tags
            results.append(res_struct)
        except ValueError:
            logger.warning(f"Invalid zettel: {f}")
    click.echo(yaml.dump(results))

commands = [list]