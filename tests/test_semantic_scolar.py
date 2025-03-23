from pyzettel.citations.semantic_scholar import Paper, get_paper

if __name__ == "__main__":
    from pprint import pprint
    import json

    json_obj = {
        # "abstract": "We give a security proof of quantum cryptography based entirely "
        # "on entanglement purification. Our proof applies to all possible "
        # "attacks (individual and coherent). It implies the security of "
        # "cryptographic keys distributed with the help of "
        # "entanglement-based quantum repeaters. We prove the security of "
        # "the obtained quantum channel which may not be used only for "
        # "quantum key distribution, but also for secure, albeit noisy, "
        # "transmission of quantum information.",
        "abstract":  None,
        "authors": [
            {"authorId": "1753179", "name": "H. Aschauer"},
            {"authorId": "32534184", "name": "H. Briegel"},
        ],
        "citationStyles": {
            "bibtex": "@Article{Aschauer2000PrivateEO,\n"
            " author = {H. Aschauer and H. Briegel},\n"
            " booktitle = {Physical Review Letters},\n"
            " journal = {Physical review letters},\n"
            " pages = {\n"
            "          047902\n"
            "        },\n"
            " title = {Private entanglement over arbitrary "
            "distances, even using noisy apparatus.},\n"
            " volume = {88 4},\n"
            " year = {2000}\n"
            "}\n"
        },
        "externalIds": {
            "ArXiv": "quant-ph/0008051",
            "CorpusId": 9295651,
            "DOI": "10.1103/PHYSREVLETT.88.047902",
            "MAG": "1976294956",
            "PubMed": "11801170",
        },
        "fieldsOfStudy": ["Computer Science", "Physics", "Medicine"],
        "influentialCitationCount": 0,
        "isOpenAccess": True,
        "openAccessPdf": {
            "status": "GREEN",
            "url": "https://arxiv.org/pdf/quant-ph/0008051",
        },
        "paperId": "999f6d648c0c5912203a14e039656ef9431b6548",
        "references": [
            {
                "paperId": None,
                "title": "in Proceedings of IEEE International Conference on Computers",
            },
            {"paperId": None, "title": "Science 283"},
            {
                "paperId": None,
                "title": "We are grateful to C. H. Bennett for pointing out "
                "this possibility",
            },
        ],
        "title": "Private entanglement over arbitrary distances, even using noisy "
        "apparatus.",
        "tldr": {
            "model": "tldr@v2.0.0",
            "text": "The security of the obtained quantum channel is proved, "
            "which may not be used only for quantum key distribution, "
            "but also for secure, albeit noisy, transmission of quantum "
            "information.",
        },
        "url": "https://www.semanticscholar.org/paper/999f6d648c0c5912203a14e039656ef9431b6548",
        "venue": "Physical Review Letters",
        "year": 2000,
    }
    #zettel.frontmatter.author = metadata.authors
    # pprint(get_paper("f41594ccb9f2747643701688e9bef050283d1055"))
    # pprint(get_paper("999f6d648c0c5912203a14e039656ef9431b6548"))
    pprint(Paper.from_json(json_doc=json.dumps(json_obj)))
