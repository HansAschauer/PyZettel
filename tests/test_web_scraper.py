from pyzettel.zettel import Zettel, Frontmatter
from pyzettel.ai.web_scraper import zettel_from_url 
from pyzettel.config import Config

from datetime import datetime
from pathlib import Path
config_file = Path(__file__).parent / "pyzettel"
config = Config.from_yaml(config_file)

def test_zettel_from_url():
    url = "https://buvis.github.io/mkdocs-zettelkasten/features/20211123214904/"
    url = "https://www.heise.de/news/KI-Update-kompakt-Thinking-Machines-Lab-Meta-Open-AI-AI-Vision-10287922.html"
    zettel = zettel_from_url(url, config)
    print(zettel.render())
    zettel.to_file(config.zettelkasten_proj_dir)
    #url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    #zettel = zettel_from_url(url, config)
    #print(zettel.render())
    
    
    
    
if __name__ == "__main__":
    test_zettel_from_url()