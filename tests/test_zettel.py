from pyzettel.zettel import Zettel, Frontmatter
from datetime import datetime

result1 = """---
date: 2025-02-18 15:52:00
id: 01951989f2b4
tags:
- hallo
- welt
title: Test

---
# Test
This is a test"""

result2 = """---
date: 2025-02-18 15:52:00
id: 01951989f2b4
tags: []
title: Test

---
# Test
This is a test

---
My footer
---
"""

result3 = """---
date: 2025-02-18 15:52:00
id: 01951989f2b4
tags: []
title: Test

---
# Test
This is a test"""
content = """# Test
This is a test"""

def setup_zettel() -> tuple[Zettel, Frontmatter]:
    frontmatter = Frontmatter(
        title="Test",
        tags=["hallo", "welt"],
        id="01951989f2b4",
        date=datetime.strptime("2025-02-18 15:52", "%Y-%m-%d %H:%M"),
    )
    z = Zettel(content=content, frontmatter=frontmatter)
    return z, frontmatter


def test_zettel():
    z, f = setup_zettel()
    print(f"__{z.render()}__")
    assert z.frontmatter == f
    assert z.content == content
    #assert z.footer == "My footer"
    assert f.tags == ["hallo", "welt"]
    assert z.render() == result1


def test_zettel_no_tags():
    z, f = setup_zettel()
    z.frontmatter.tags = []
    z.footer = "My footer"
    print(z.render())
    assert z.render() == result2


def test_zettel_no_footer():
    z,f = setup_zettel()
    z.footer = ""
    z.frontmatter.tags = []
    print(f"__{z.render()}__")
    assert z.render() == result3

def test_parse_zettel():
    for z_txt in result1, result2, result3:
        print(z_txt)
        z = Zettel.from_string(z_txt)
        print(z.render())
        assert z_txt.strip() == z.render().strip()