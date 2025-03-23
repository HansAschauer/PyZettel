from ..zettel import Zettel, Frontmatter
from ..config import Config
from .doi import bibtex_from_doi
import requests


from .opencitations import references, citations
from .semantic_scholar import get_paper
from .crossref import get_refstring

import pathlib
import logging

logger = logging.getLogger(__name__)


def zettel_from_doi(
    doi: str,
    config: Config,
    download: bool = False,
    get_references: bool = True,
    get_citations: bool = False,
    add_to_bibtex: bool = True,
) -> Zettel | None:
    # print(f"zettel_from_doi for DOI {doi}")
    bibtex_entry = bibtex_from_doi(doi)
    #metadata = Metadata(doi)
    try:
        paper = get_paper(doi)
    except Exception as e:
        logging.error(f"Error getting paper from Semantic Scholar: {e}")
        return None
    if not paper.title:
        title = "No title"
    else:
        title = paper.title
    # print(f"Title: {title}")
    frotmatter = Frontmatter(title, _id_template=config.id_template)
    zettel = Zettel(frotmatter)
    zettel.frontmatter.tags = ["paper"]
    if paper.authors:
        authors = ", ".join([author.name for author in paper.authors])
        zettel.frontmatter.author = authors

    zettel_content = [f"# {title}\n**{authors}**"]
    if paper.abstract is not None:
        zettel_content.append("\n### Abstract\n" + paper.abstract)
    if paper.tldr is not None:
        zettel_content.append("\n### TL;DR\n" + paper.tldr.text)
    if get_references:
        refs = references(doi)
        if refs:
            print("generating references")
            zettel_content.append("\n### References")
            for ref in refs:
                print(f"- {ref}")
                if ref.cited:
                    #ref_meta = Metadata(ref.cited)
                    #zettel_content.append(f"- {ref_meta.write(to='citation')}")
                    try:
                        cited_ref = get_refstring(ref.cited)
                        if cited_ref:
                            zettel_content.append(f"- {cited_ref}")
                    except ValueError as e:
                        logging.warning(f"Error getting reference string: {e}")
                else:
                    logging.warning(
                        f"No DOI for reference with oci={ref.oci} provided by Opencitations.org"
                    )
    if get_citations:
        cits = citations(doi)
        if cits:
            print("generating citations")
            zettel_content.append("\n### Citations")
            for cit in cits:
                print(f"- {cit}")
                if cit.citing:
                    #cit_meta = Metadata(cit.citing)
                    #zettel_content.append(f"- {cit_meta.write(to='citation')}")
                    try:
                        citing_ref = get_refstring(cit.citing)
                        if citing_ref:
                            zettel_content.append(f"- {citing_ref}")
                    except ValueError as e:
                        logging.warning(f"Error getting reference string: {e}")
                else:
                    logging.warning(
                        f"No DOI for citation with oci={cit.oci} provided by Opencitations.org"
                    )

    if bibtex_entry:
        zettel_content.append(f"\n### Bibtex\n```bibtex\n{bibtex_entry}```")
    zettel.content = "\n".join(zettel_content)
    if paper.openAccessPdf is not None and paper.openAccessPdf.status == "GREEN":
        if download and config.zettelkasten_paper_dir != "":
            result = requests.get(paper.openAccessPdf.url)
            if (
                result.status_code == 200
                and result.headers["content-type"] == "application/pdf"
            ):
                paper_dir = pathlib.Path(config.zettelkasten_paper_dir)
                paper_dir.mkdir(parents=True, exist_ok=True)
                pdf_filename = paper_dir / f"{zettel.frontmatter.id}.pdf"
                with open(pdf_filename, "wb") as f:
                    f.write(result.content)
                    zettel.footer = f"[Local PDF]{pdf_filename}"
                    # common_sub = os.path.commonpath([config.zettelkasten_paper_dir, config.zettelkasten_proj_dir])
                    # zettel.footer = f"[Local PDF]({os.path.relpath(pdf_filename, common_sub)})"

        else:
            zettel.footer = f"[Download PDF]({paper.openAccessPdf.url})"
    return zettel
