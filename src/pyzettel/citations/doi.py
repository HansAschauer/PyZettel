import requests
import bibtexparser
from ..cache import open_cache


def bibtex_from_doi(doi: str, bibtex_key: str | None = None) -> str | None:
    """
    Get a bibtex entry from a DOI
    :param doi: The DOI
    :param bibtex_key: The bibtex key to use
    :return: The bibtex entry
    """
    doi = doi.lower()
    with open_cache("doi") as cache:
        if doi in cache:
            return cache[doi]
        url = f"http://dx.doi.org/{doi}"
        response = requests.get(
            url, headers={"Accept": "text/bibliography; style=bibtex"}
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return None
        bibtex = response.content.decode(response.apparent_encoding)
        parsed_result = bibtexparser.loads(bibtex)
        if bibtex_key is not None:
            parsed_result.entries[0].key = bibtex_key
        res = bibtexparser.dumps(parsed_result)
        if res:
            cache[doi] = res
        return res
