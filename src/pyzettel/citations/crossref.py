
from ..cache import use_cache
import requests

import re

rx = re.compile(r"\[\d*\](.*)")

@use_cache("crossref")
def get_refstring(doi: str, style="ieee") -> str:
    headers = {"Accept": f"text/x-bibliography; style={style}"}
    try:
        res = requests.get(
            f"https://api.crossref.org/works/{doi}/transform",
            headers=headers,
        )
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"Error code {res.status_code} getting reference string: {e}")
    formatted = res.content.decode(res.apparent_encoding).strip()
    m = rx.match(formatted)
    if m:
        return m.group(1)
    return formatted