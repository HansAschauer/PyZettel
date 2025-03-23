from dataclasses import dataclass, field
from pyzettel.utils import YAMLSerializable

import re
from contextlib import contextmanager
from typing import Self
from collections.abc import Iterator
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

@dataclass
class Tag:
    zettels: list[str]
    embedding: str


@dataclass
class Tagsfile(YAMLSerializable):
    tags: dict[str, Tag] = field(default_factory=dict)

    def match(self, regexp: str) -> list[str]:
        regexp_comp = re.compile(regexp)
        return [tag for tag in self.tags.keys() if regexp_comp.match(tag)]

    # Got the type annotation from https://stackoverflow.com/a/70277752
    @classmethod
    @contextmanager
    def use(cls, filename: str | Path) -> Iterator[Self]:
        filename = Path(filename)
        logger.debug(f"Using tagsfile {filename}")
        if not filename.exists():
            with open(filename, "w") as f:
                f.write(cls().to_yaml())
        with open(filename) as f:
            tagsfile = cls.from_yaml(f)
        try:
            yield tagsfile
        finally:
            with open(filename, "w") as f:
                f.write(tagsfile.to_yaml())
