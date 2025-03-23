from ..config import Config
from re import compile
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

tags_expr = compile(r'## <span class="tag">([\w\- ]*)</span>')


def get_tags(config: Config) -> list[str]:
    tags_filename = Path(config.zettelkasten_proj_dir) / "aux" / "tags.md"
    if not tags_filename.exists():
        logger.info(f"Tags file {tags_filename} does not exist. Maybe you do not have a running mkdocs installation?")
        return []
    tags: list[str] = []
    with open(tags_filename,"r") as f:
        for line in f:
            if (m := tags_expr.match(line)) is not None:
                tags.append(m.group(1))
    return tags