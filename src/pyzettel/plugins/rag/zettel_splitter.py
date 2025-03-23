import pathlib
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownTextSplitter
from pyzettel.zettel import Zettel
from logging import getLogger
logger = getLogger(__name__)

splitter = MarkdownTextSplitter()


def zettel_to_docs(
    zettel_filename: str | pathlib.Path,
) -> tuple[list[Document], list[str]]:
    mtime = pathlib.Path(zettel_filename).stat().st_mtime
    try:
        zettel = Zettel.from_file(zettel_filename)
    except ValueError:
        logger.warning(f"Invalid zettel: {zettel_filename}")
        return [], []
    meta = dict(mtime=mtime)
    doc = Document(page_content=zettel.content, metadata=meta)
    splits = splitter.split_documents([doc])
    ids = [f"{zettel.frontmatter.id}_{i}" for i in range(len(splits))]
    for i, split in enumerate(splits):
        split.metadata["zettel_id"] = zettel.frontmatter.id
        split.metadata["title"] = zettel.frontmatter.title
        split.metadata["zettel_split"] = "%05i" % i
        split.metadata["type"] = "split"
    for i, tag in enumerate(zettel.frontmatter.tags):
        meta = dict(
            zettel_id=zettel.frontmatter.id, type="tag", title=zettel.frontmatter.title
        )
        doc = Document(page_content=tag, metadata=meta)
        print("tag doc", doc)
        splits.append(doc)
        ids.append(f"{zettel.frontmatter.id}_tag_{i:0>3}")
    return splits, ids
