from dataclasses import dataclass, field
from pyzettel.utils import YAMLSerializable, filename_from_id
from pyzettel.zettel import Zettel
from pyzettel.config import Config
from ...ai.embeddings import embedding_to_string
from pyzettel.cli.plugins import get_embedder_factory
from contextlib import contextmanager
from typing import Self
from collections.abc import Iterator
from pathlib import Path
from hashlib import sha256
from langchain_core.embeddings import Embeddings
import logging

logger = logging.getLogger(__name__)


@dataclass
class ZettelIndexEntry:
    zettel_id: str
    mtime: float
    embedding_title: str
    embedding_content: str
    zettel_content_hash: str

    @classmethod
    def from_zettel(
        cls,
        zettel: Zettel,
        config: Config,
        embedder: Embeddings | None = None,
    ) -> Self:
        z_id = zettel.frontmatter.id
        f_name = Path(filename_from_id(z_id, config))
        mtime = f_name.stat().st_mtime
        hash = cls.calc_hash(zettel.content)
        if embedder is None:
            embedder = get_embedder_factory()()
        embedding_content = embedder.embed_documents([zettel.content])[0]
        embedding_title = embedder.embed_documents([zettel.frontmatter.title])[0]
        return cls(
            z_id,
            mtime,
            embedding_to_string(embedding_title),
            embedding_to_string(embedding_content),
            hash,
        )

    @staticmethod
    def calc_hash(string: str):
        return sha256(string.replace("\n", " ").encode()).hexdigest()


@dataclass
class ZettelIndex(YAMLSerializable):
    zettel_entries: dict[str, ZettelIndexEntry] = field(default_factory=dict)

    # Got the type annotation from https://stackoverflow.com/a/70277752
    @classmethod
    @contextmanager
    def use(cls, filename: str | Path) -> Iterator[Self]:
        filename = Path(filename)
        logger.debug(f"Using zettel index file {filename}")
        if not filename.exists():
            with open(filename, "w") as f:
                f.write(cls().to_yaml())
        with open(filename) as f:
            zettel_index = cls.from_yaml(f)
        try:
            yield zettel_index
        finally:
            with open(filename, "w") as f:
                f.write(zettel_index.to_yaml())

    def add_or_update_zettel(
        self,
        zettel: Zettel,
        config: Config,
        embedding: Embeddings | None = None,
    ):
        if zettel.frontmatter.id in self.zettel_entries:
            zie = self.zettel_entries[zettel.frontmatter.id]
            f_name = Path(filename_from_id(zettel.frontmatter.id, config))
            mtime = f_name.stat().st_mtime
            if (mtime == zie.mtime) and (
                ZettelIndexEntry.calc_hash(zettel.content) == zie.zettel_content_hash
            ):
                return
        zie = ZettelIndexEntry.from_zettel(zettel, config, embedding)
        self.zettel_entries[zettel.frontmatter.id] = zie
