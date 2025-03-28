from ...ai.embeddings import embedding_from_string
from pyzettel.exceptions import ZettelNotFound
from pyzettel.utils import filename_from_id
from pyzettel.zettel import Zettel
from pyzettel.config import Config
from pyzettel.cli.plugins import get_embedder_factory, RessourceNotFound
from .models import ZettelIndex
import click
import numpy as np
import pathlib

import logging

logger = logging.getLogger(__name__)


def get_zettel_index_file_name(config: Config) -> pathlib.Path:
    """
    Returns the path to the zettel index file.

    Args:
        config (Config): The configuration object.

    Returns:
        pathlib.Path: The path to the zettel index file.
    """
    aux_dir = (
        pathlib.Path(config.zettelkasten_proj_dir) / config.zettelkasten_subdir / "aux"
    )
    aux_dir.mkdir(parents=True, exist_ok=True)
    return aux_dir / "zettel_index.yaml"


@click.command()
@click.pass_context
def update(ctx: click.Context):
    config = ctx.obj.config

    zettelkasten_dir = (
        pathlib.Path(config.zettelkasten_proj_dir) / config.zettelkasten_subdir
    )

    ai_options = config.ai_options
    assert ai_options is not None
    embedder = get_embedder_factory()()

    with ZettelIndex.use(get_zettel_index_file_name(config)) as zettel_index:
        for f in zettelkasten_dir.glob("*.md"):
            logger.debug(f"Using file {f}")
            try:
                z = Zettel.from_file(f)
                logger.debug(
                    f"Generate or update index for zettel {z.frontmatter.id}, {z.frontmatter.title}"
                )
                zettel_index.add_or_update_zettel(z, config, embedder)
            except ValueError:
                logger.warning(f"File {f} is not in valid zettel format.")


@click.command()
@click.argument("search_string")
@click.pass_context
def search(ctx: click.Context, search_string: str):
    "Perform semantic search, using 'SEARCH_STRING'"
    config = ctx.obj.config
    embedder = get_embedder_factory()()

    search_embedding = embedder.embed_query(search_string)

    with ZettelIndex.use(get_zettel_index_file_name(config)) as zettel_index:
        title_embeddings = [
            embedding_from_string(z.embedding_title)
            for z in zettel_index.zettel_entries.values()
        ]
        content_embeddings = [
            embedding_from_string(z.embedding_content)
            for z in zettel_index.zettel_entries.values()
        ]

        zettel_ids = [z.zettel_id for z in zettel_index.zettel_entries.values()]

    title_mtx = np.array(title_embeddings) / np.linalg.norm(
        title_embeddings, axis=1
    ).reshape(-1, 1)
    content_mtx = np.array(content_embeddings) / np.linalg.norm(
        content_embeddings, axis=1
    ).reshape(-1, 1)
    search_embedding = search_embedding / np.linalg.norm(search_embedding).reshape(
        -1, 1
    )
    title_sim = np.matmul(title_mtx, search_embedding.reshape(-1, 1)).flatten()
    content_sim = np.matmul(content_mtx, search_embedding.reshape(-1, 1)).flatten()

    title_sorted = list(reversed(sorted(zip(title_sim, zettel_ids))))
    content_sorted = list(reversed(sorted(zip(content_sim, zettel_ids))))

    click.echo(f"Top ranked zettels for search {search_string}:")
    click.echo(" - searching titles:")
    for i in range(min(10, len(title_sorted))):
        try:
            z = Zettel.from_file(filename_from_id(title_sorted[i][1], config))
        except ZettelNotFound:
            logger.warning(
                f"Zettel {title_sorted[i][1]} not found, skipping from search results"
            )
            continue
        click.echo(
            f"  {title_sorted[i][0]:.2f}% {z.frontmatter.id} {z.frontmatter.title}"
        )
    click.echo(" - searching fulltext:")
    for i in range(min(10, len(content_sorted))):
        try:
            z = Zettel.from_file(filename_from_id(content_sorted[i][1], config))
        except ZettelNotFound:
            logger.warning(
                f"Zettel {content_sorted[i][1]} not found, skipping from search results"
            )
            continue
        click.echo(
            f"  {content_sorted[i][0]:.2f}% {z.frontmatter.id} {z.frontmatter.title}"
        )


@click.group()
def index():
    pass


index.add_command(update)

commands = [search, index]
