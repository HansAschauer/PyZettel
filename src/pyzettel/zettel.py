from dataclasses import dataclass, field, asdict
from .utils import generate_id, filename_from_id
from .config import Config
from .exceptions import ZettelNotFound
import jinja2
import re
import yaml
import datetime
import pathlib
import logging
from contextlib import contextmanager
from typing import Self
from collections.abc import Iterator

logger = logging.getLogger(__name__)


delim = re.compile(r"---\s*", re.MULTILINE)


zettel_template = """---
{{ frontmatter_yaml }}
---
{{ content -}}
{% if footer %}

---
{{ footer }}
---
{% endif -%}"""


@dataclass
class Frontmatter:
    title: str
    id: str = ""
    _id_template: str = ""
    tags: list[str] = field(default_factory=list)
    date: datetime.datetime | None = None
    ai_generated: bool = False
    author: str = ""
    _additional_attributes: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        if self.id == "":
            if self._id_template == "":
                raise ValueError("No id or id_template provided")
            self.id = generate_id(self._id_template)

        if self.date is None:
            self.date = datetime.datetime.now()


@dataclass
class Zettel:
    frontmatter: Frontmatter
    content: str = ""
    footer: str = ""

    def render(self) -> str:
        template = jinja2.Template(zettel_template)
        frontmatter_dict = {
            key: value
            for (key, value) in asdict(self.frontmatter).items()
            if not key.startswith("_")
        }
        frontmatter_dict.update(self.frontmatter._additional_attributes)
        frontmatter_yaml = yaml.dump(frontmatter_dict, allow_unicode=True)
        return template.render(
            frontmatter_yaml=frontmatter_yaml,
            content=self.content,
            footer=self.footer,
        )

    def to_file(self, zettelkasten_dir: pathlib.Path | str):
        zettelkasten_dir = pathlib.Path(zettelkasten_dir)
        file_path = zettelkasten_dir / f"{self.frontmatter.id}.md"
        with open(file_path, "w") as f:
            f.write(self.render())  

    @classmethod
    def from_file(cls, file_path: str | pathlib.Path) -> Self:
        try:
            with open(file_path, "r") as f:
                content = f.read()
            return cls.from_string(content)
        except FileNotFoundError:
            raise ZettelNotFound(f"Zettel file {file_path} not found")
    @classmethod
    def from_string(cls, content: str) -> Self:
        parts = delim.split(content)
        if len(parts) < 3:
            raise ValueError("Invalid Zettel format: no valid frontmatter")
        if parts[0] != "":
            raise ValueError("Invalid Zettel format: data before frontmatter")
        frontmatter = Frontmatter(**yaml.safe_load(parts[1]))
        parts.pop(0)  # empty string
        parts.pop(0)  # frontmatter

        if len(parts) >= 3 and parts[-1] == "":
            footer = parts[-2].strip()
            parts.pop(-1)
            parts.pop(-1)
        else:
            footer = ""
        content = "---\n".join([p.strip() for p in parts])
        return cls(frontmatter=frontmatter, content=content, footer=footer)

    def write_to_zettelfile(self, config: Config) -> str:
        zettel_file = filename_from_id(self.frontmatter.id, config)
        with open(zettel_file, "w") as f:
            f.write(self.render())
        return zettel_file
    
    @classmethod
    @contextmanager
    def use_zettel(cls, zettel_id: str, config: Config) -> Iterator[Self]:
        zettel_file = filename_from_id(zettel_id, config)
        z = cls.from_file(zettel_file)
        yield z
        with open(zettel_file, "w") as f:
            f.write(z.render())
        