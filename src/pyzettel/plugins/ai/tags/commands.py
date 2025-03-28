import yaml
import click
from pyzettel.zettel import Zettel
from .models import Tagsfile, Tag
from .utils import replace_tag_in_zettel, get_tagsfile_name
from pyzettel.utils import filename_from_id
from ...ai.embeddings import (
    embedding_from_string,
    embedding_to_string,
    similarity_matrix,
)
from langchain_core.embeddings import Embeddings
from pyzettel.cli.plugins import get_embedder_factory, RessourceNotFound
import pathlib
import numpy as np

import logging

logger = logging.getLogger(__name__)

# alias for built-in type (since we override `list` below)
python_list = list


@click.command()
@click.option(
    "--regexp",
    "-r",
    default=".*",
    help="List tags matching this regex.",
)
@click.option(
    "--show-zettel-title/--no-show-zettel-title",
    "-s/-S",
    is_flag=True,
    help="show zettels which have the tag.",
)
@click.option(
    "--show-zettel-id/--no-show-zettel-id",
    "-i/-I",
    help = "show IDs of tagged zettels"
)
@click.pass_context
def list(ctx: click.Context, regexp: str, show_zettel_title: bool, show_zettel_id: bool):
    logger.debug(f"Listing tags matching {regexp}, show_zettel_title={show_zettel_title}")
    config = ctx.obj.config
    tags_file = get_tagsfile_name(config)
    with Tagsfile.use(tags_file) as tagsfile:
        tags = tagsfile.match(regexp)
        if show_zettel_title or show_zettel_id:
            for tag in tags:
                zettels = tagsfile.tags[tag].zettels
                titles = []
                for zettel_id in zettels:
                    zettel_file = filename_from_id(zettel_id, config)
                    z = Zettel.from_file(zettel_file)
                    match (show_zettel_title, show_zettel_id):
                        case (True, True):
                            t = f"[{z.frontmatter.title}]({z.frontmatter.id})"
                        case (True, False):
                            t = z.frontmatter.title
                        case (False, True):
                            t = z.frontmatter.id
                        case _:
                            raise ValueError("This should not happen.")
                    titles.append(t)
                click.echo(f"{tag}:\n - {'\n - '.join(titles)}")
        else:
            click.echo(yaml.dump(python_list(set(tags))))


@click.command()
@click.option("--similarity-cutoff", "-s", default=0.8, help="Cutoff for similarity")
@click.pass_context
def find_similar(ctx: click.Context, similarity_cutoff: float = 0.8):
    config = ctx.obj.config
    tags_file = get_tagsfile_name(config)
    with Tagsfile.use(tags_file) as tagsfile:
        embeddings = [
            embedding_from_string(t.embedding) for t in tagsfile.tags.values()
        ]
        tags = python_list(tagsfile.tags.keys())
        sim_mtx = similarity_matrix(embeddings)
        ii1, ii2 = np.where((sim_mtx > similarity_cutoff) & (sim_mtx < 0.9999999999999))
        indices = [(i1, i2) for i1, i2 in zip(ii1, ii2) if i1 < i2]
        sim_list = reversed(
            sorted([(sim_mtx[i1, i2], tags[i1], tags[i2]) for i1, i2 in indices])
        )
        for sim_val, t1, t2 in sim_list:
            click.echo(f"{t1} and {t2} are similar with similarity {sim_val:.2f}")


@click.command()
@click.argument("tag-spec")
@click.pass_context
def replace(ctx: click.Context, tag_spec: str):
    """
    Replace a tag with another tag in all zettels. TAG_SPEC is in the format <tag_to_replace>:<tag_replacement>"""
    tagstr_to_replace, tagstr_replacement = tag_spec.split(":")
    config = ctx.obj.config
    with Tagsfile.use(get_tagsfile_name(config)) as tagsfile:
        tag_to_replace = tagsfile.tags.get(tagstr_to_replace)
        tag_replacement = tagsfile.tags.get(tagstr_replacement)
        if tag_replacement is None:
            logger.debug(f"Tag {tagstr_replacement} not found in tagsfile")
            click.echo(f"Tag {tagstr_replacement} not found in tagsfile. Exiting.")
            return
        if tag_to_replace is None:
            logger.error(f"Tag {tagstr_to_replace} not found in tagsfile")
            return
        for zettel_id in tag_to_replace.zettels:
            replace_tag_in_zettel(
                zettel_id, tagstr_to_replace, tagstr_replacement, config
            )
            if zettel_id not in tag_replacement.zettels:
                tag_replacement.zettels.append(zettel_id)
        del tagsfile.tags[tagstr_to_replace]


@click.command()
@click.pass_context
def sync(ctx: click.Context):
    """Sync tags in tagsfile with PyZettel's tags database"""
    embedder: Embeddings | None = None
    config = ctx.obj.config
    tags_file = get_tagsfile_name(config)
    try:
        embedder = get_embedder_factory()()
    except RessourceNotFound:
        logger.info("Embedder not found")
        embedder = None
    with Tagsfile.use(tags_file) as tagsfile:
        zettelkasten_dir = (
            pathlib.Path(config.zettelkasten_proj_dir) / config.zettelkasten_subdir
        )
        for f in zettelkasten_dir.glob("*.md"):
            try:
                z = Zettel.from_file(f)
            except ValueError:
                logger.warning(f"Zettel {f} is not in valid format")
                continue
            tags = z.frontmatter.tags
            for tag_string in tags:
                if tag_string not in tagsfile.tags:
                    logger.debug(f"Adding tag {tag_string}")
                    if embedder is not None:
                        logger.debug(f"Getting embedding for tag {tag_string}")
                        embedding = embedding_to_string(
                            embedder.embed_documents([tag_string])[0]
                        )
                    else:
                        embedding = ""
                    tag = Tag(zettels=[z.frontmatter.id], embedding=embedding)
                    tagsfile.tags[tag_string] = tag
                else:
                    if z.frontmatter.id not in tagsfile.tags[tag_string].zettels:
                        logger.debug(
                            f"Adding zettel {z.frontmatter.id} to tag {tag_string}"
                        )
                        tagsfile.tags[tag_string].zettels.append(z.frontmatter.id)


@click.group
def tags():
    pass


tags.add_command(list)
tags.add_command(sync)
tags.add_command(find_similar)
tags.add_command(replace)

commands = [tags]