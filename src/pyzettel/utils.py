from cattrs.preconf.pyyaml import make_converter
import yaml
import json
import jinja2

import datetime
from dataclasses import dataclass
from typing import TextIO, Self, TYPE_CHECKING
import pathlib
import logging
import uuid

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .config import Config


def iso_from_datetime(dt: datetime.datetime) -> str:
    return dt.replace(microsecond=0).isoformat()


def hexdate(value: datetime.datetime, num_digits=12, factor=1000) -> str:
    ts = value.timestamp()
    return (
        int(ts * factor)
        .to_bytes(int((num_digits + 1) / 2), byteorder="big")
        .hex()[-num_digits:]
    )


def intdate(value: datetime.datetime, num_digits=14, factor=1000) -> str:
    ts = value.timestamp()
    return str(int(ts * factor)).rjust(num_digits, "0")


env = jinja2.Environment()
env.filters["hexdate"] = hexdate
env.filters["intdate"] = intdate


def generate_id(
    id_template: str, now: datetime.datetime | None = None, my_uuid: uuid.UUID | None = None
) -> str:
    template = env.from_string(id_template)
    if now is None:
        now = datetime.datetime.now()
    if my_uuid is None:
        my_uuid = uuid.uuid4()
    return template.render(now=now, uuid=my_uuid)


def filename_from_id(id: str, config: "Config") -> str:
    zettel_dir = pathlib.Path(config.zettelkasten_proj_dir) / config.zettelkasten_subdir
    return str(zettel_dir / f"{id}.md")    

    
    

converter = make_converter()

@dataclass
class YAMLSerializable:
    @classmethod
    def from_yaml(
        cls, yaml_file: pathlib.Path | TextIO | None = None, yaml_doc: str | None = None
    ) -> Self:
        match (yaml_file, yaml_doc):
            case (None, None):
                raise ValueError(
                    "Either yaml_file or yaml_doc must be given and non-empty."
                )
            case (None, yaml_doc):
                pass
            case (pathlib.Path(), _):
                yaml_file = open(yaml_file, "r")
                yaml_doc = yaml_file.read()
            case _:
                try:
                    yaml_doc = yaml_file.read()  # type: ignore
                except Exception:
                    raise ValueError("Cannot not read() from provided yaml_file object")
        assert yaml_doc
        return converter.structure(yaml.safe_load(yaml_doc), cls)

    def to_yaml(self) -> str:
        return yaml.safe_dump(converter.unstructure(self))

class JSONSerializable:
    @classmethod
    def from_json(
        cls, json_file: pathlib.Path | TextIO | None = None, json_doc: str | None = None
    ) -> Self:
        match (json_file, json_doc):
            case (None, None):
                raise ValueError(
                    "Either json_file or json_doc must be given and non-empty."
                )
            case (None, json_doc):
                pass
            case (pathlib.Path(), _):
                json_file = open(json_file, "r")
                json_doc = json_file.read()
            case _:
                try:
                    json_doc = json_file.read()  # type: ignore
                except Exception:
                    raise ValueError("Cannot not read() from provided json_file object")
        assert json_doc
        return converter.structure(json.loads(json_doc), cls)

    def to_json(self, indent: int| str|None = None) -> str:
        return json.dumps(converter.unstructure(self), indent=indent)
