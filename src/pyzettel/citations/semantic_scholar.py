import requests
from dataclasses import dataclass
from typing import List, Optional, Dict

from ..utils import YAMLSerializable, JSONSerializable
from ..cache import open_cache


@dataclass
class Author:
    authorId: str
    name: str


@dataclass
class CitationStyles:
    bibtex: str


@dataclass
class ExternalIds:
    ArXiv: Optional[str]
    CorpusId: Optional[int]
    DOI: Optional[str]
    MAG: Optional[str]
    PubMed: Optional[str]


@dataclass
class OpenAccessPdf:
    status: str
    url: str


@dataclass
class Reference:
    paperId: Optional[str]
    title: str


@dataclass
class TLDR:
    model: str
    text: str


@dataclass
class Paper(JSONSerializable):
    abstract: str | None
    authors: List[Author]
    citationStyles: CitationStyles | None
    externalIds: dict[str, str]
    fieldsOfStudy: List[str]
    influentialCitationCount: int
    isOpenAccess: bool
    openAccessPdf: OpenAccessPdf | None
    paperId: str
    references: List[Reference]
    title: str | None
    tldr: TLDR | None
    url: str | None
    venue: str | None
    year: int | None


api_base_url = "https://api.semanticscholar.org/graph/v1"
fields = [
    "abstract",
    "authors",
    "citationStyles",
    "externalIds",
    "fieldsOfStudy",
    "influentialCitationCount",
    "isOpenAccess",
    "openAccessPdf",
    "references",
    "title",
    "tldr",
    "url",
    "venue",
    "year",
]


def get_paper(doi: str) -> Paper:
    doi = doi.lower()
    with open_cache("semantic_scholar") as cache:
        if doi in cache:
            return Paper.from_json(json_doc=cache[doi])
    
        url = f"{api_base_url}/paper/DOI:{doi}?fields={','.join(fields)}"
        response = requests.get(url)
        json_doc = response.text
        paper = Paper.from_json(json_doc=json_doc)
        if paper:
            cache[doi] = json_doc
    return paper
    

