from pyzettel.plugins.rag.cli import init_db
from pyzettel.plugins.rag.cli import ask
from pyzettel.plugins.rag.cli import update

def test_init_db():
    assert init_db() == None

if __name__ == '__main__':
    test_init_db()
    print("init_db passed")