from pyzettel.citations import opencitations
from pyzettel.utils import converter
from pyzettel.config import Config
from pathlib import Path

config_file = Path(__file__).parent / "pyzettel"
config = Config.from_yaml(config_file)
api_key = config.opencitations_api_key
import json

results = """[
    {
        "creation": "2003-06-30",
        "timespan": "P1Y5M21D",
        "cited": "10.1103/physrevlett.88.047902",
        "journal_sc": "no",
        "author_sc": "no",
        "oci": "06101350947-061703510303",
        "citing": "10.1103/physreva.67.062320"
    },
    {
        "creation": "2012-05-11",
        "timespan": "P10Y4M2D",
        "cited": "10.1103/physrevlett.88.047902",
        "journal_sc": "no",
        "author_sc": "no",
        "oci": "06101414740-061703510303",
        "citing": "10.1103/revmodphys.84.777"
    },
    {
        "creation": "2009-06-17",
        "timespan": "P7Y5M8D",
        "cited": "10.1103/physrevlett.88.047902",
        "journal_sc": "no",
        "author_sc": "no",
        "oci": "06101414915-061703510303",
        "citing": "10.1103/revmodphys.81.865"
    }
]
"""


def test_to_joson():
    citation = opencitations.OpenCitationsCitation(
        creation="2003-06-30",
        timespan="P1Y5M21D",
        cited="10.1103/physrevlett.88.047902",
        journal_sc="no",
        author_sc="no",
        oci="06101350947-061703510303",
        citing="10.1103/physreva.67.062320"
    )
    assert citation.to_json(indent=4) == """{
    "creation": "2003-06-30",
    "timespan": "P1Y5M21D",
    "cited": "10.1103/physrevlett.88.047902",
    "journal_sc": "no",
    "author_sc": "no",
    "oci": "06101350947-061703510303",
    "citing": "10.1103/physreva.67.062320"
}"""
    results_obj = [citation]
    print(converter.unstructure(results_obj))
    
def test_from_json():
    result = converter.structure(json.loads(results), list[opencitations.OpenCitationsCitation])
    assert len(result) == 3
    print(result)
    
def test_from_doi():
    result = opencitations.citations("10.1103/physrevlett.88.047902", api_key)
    assert len(result) == 26
    print(result)
    result = opencitations.references("10.1103/physrevlett.88.047902", api_key)
    assert len(result) == 13
    print(result)
    
if __name__ =="__main__":
    test_from_doi()