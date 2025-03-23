import click
from ...citations.zettel_from_doi import zettel_from_doi

import subprocess



@click.command()
@click.option("--doi", "-d", required=True, help="DOI of paper to retrieve")
@click.option(
    "--tag",
    "-g",
    multiple=True,
    help="Tags for the zettel. Will be added to the auto generated tags.",
)
@click.option(
    "--generate-references/-no-generate-references",
    "-r/-R",
    is_flag=True,
    default=True,
    help="Generate references for the publication",
)
@click.option(
    "--generate-citations/-no-generate-citations",
    "-c/-C",
    is_flag=True,
    default=False,
    help="Generate citations for the publication",
)
@click.option(
    "--generate-bibtex/-no-generate-bibtex",
    "-b/-B",
    is_flag=True,
    default=True,
    help="Generate bibtex for the publication",
)
@click.option("--add-to-bibtex/--no-add-to-bibtex", "-a/-A", is_flag=True, default=True)
@click.option("--download/--no-download", "-w/-W", is_flag=True, default=False)
# @click.option("--bibtex-entry", "-b", help="Bibtex entry for the paper")
@click.pass_context

def paper(
    ctx: click.Context,
    doi: str,
    tag: list[str],
    add_to_bibtex: bool,
    download: bool, 
    generate_references: bool,
    generate_citations: bool,
    generate_bibtex: bool,
):
    """Create a zettel from a paper DOI"""
    config = ctx.obj.config

    z = zettel_from_doi(
        doi, config, download, generate_references, generate_citations, add_to_bibtex
    )
    if z is None:  # an error occurred
        return
    z.frontmatter.tags = list(set(tag) | set(z.frontmatter.tags))

    zettel_file = z.write_to_zettelfile(config)

    click.echo(f"Created zettel at {zettel_file}")


    args = [config.editor] + config.editor_args + [zettel_file]
    subprocess.Popen(args)

commands = [paper]