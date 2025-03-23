from pyzettel.config import Config
from pyzettel.zettel import Zettel

import pathlib

def replace_tag_in_zettel(
    zettel_id: str, tag_to_replace: str, tag_replacement: str, config: Config
) -> None:
    """
    Replaces a tag in a specific zettel with a new tag.

    Args:
        zettel_id (str): The unique identifier of the zettel where the tag needs to be replaced.
        tag_to_replace (str): The tag that needs to be replaced.
        tag_replacement (str): The new tag that will replace the old tag.

    Returns:
        None
    """
    with Zettel.use_zettel(zettel_id, config) as zettel:
        zettel.frontmatter.tags = [
            tag_replacement if tag == tag_to_replace else tag
            for tag in zettel.frontmatter.tags
        ]
        
def get_tagsfile_name(config: Config) -> pathlib.Path:
    """
    Returns the path to the tags file.

    Args:
        config (Config): The configuration object.

    Returns:
        pathlib.Path: The path to the tags file.
    """
    aux_dir = pathlib.Path(config.zettelkasten_proj_dir) / config.zettelkasten_subdir / "aux"
    aux_dir.mkdir(parents=True, exist_ok=True)
    return aux_dir / "tags.yaml"
