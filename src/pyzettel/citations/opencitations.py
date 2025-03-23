from dataclasses import dataclass, field
from ..utils import JSONSerializable, converter
from ..cache import open_cache
import requests
import json
from typing import Literal


@dataclass
class OpenCitationsCitation(JSONSerializable):
    creation: str
    timespan: str
    cited: str
    journal_sc: str
    author_sc: str
    oci: str
    citing: str


def is_doi(doi_or_oci: str) -> bool:
    """Check if a string is a DOI or an OCI.

    Args:
        doi_or_oci (str): The string to check

    Returns:
        bool: True if the string is a DOI, False if it is an OCI. Undefined if it is neither.
    """
    return doi_or_oci.startswith("10.")


# def get_opencitations_from_url(url: str) -> list[OpenCitationsCitation]:
#    response = requests.get(url)
#    response.raise_for_status()
#    return converter.structure(json.loads(response.text), list[OpenCitationsCitation])


def get_opencitations_from_doi(
    doi_or_oci: str,
    kind: Literal["citations", "references"],
    api_key: str | None = None,
) -> list[OpenCitationsCitation]:
    with open_cache(f"opencitations_{kind}") as cache:
        if doi_or_oci.lower() in cache:
            return cache[doi_or_oci.lower()]
        url = f"https://opencitations.net/index/api/v1/{kind}/{doi_or_oci}"
        if api_key is not None:
            headers = {"authorization": api_key}
        else:
            headers = {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res = converter.structure(
            json.loads(response.text), list[OpenCitationsCitation]
        )
        if is_doi(doi_or_oci) and res:
            cache[doi_or_oci.lower()] = res
    return res


def citations(
    doi_or_oci: str, api_key: str | None = None
) -> list[OpenCitationsCitation]:
    return get_opencitations_from_doi(doi_or_oci, "citations", api_key)


def references(doi_or_oci, api_key: str | None = None) -> list[OpenCitationsCitation]:
    return get_opencitations_from_doi(doi_or_oci, "references", api_key)
