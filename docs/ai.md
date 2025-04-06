## AI command group

The commands in this group employ LLM and embedding models for the following tasks:

- `create`: This command allows you to create new zettels from scratch, using a
  LLM. You provide the title of the zettel (`--title`/`-t`), and optionally
  additional input (`--additional-input`/`-i`), and the LLM generates a new
  zettel, along with a selection of tags.

- `improve`: Improve an existing zettel, using a LLM. `--regards`/`-r` allows
  you to tell the LLM, in which regards you want the improvement (can be given
  several times). This command can also be used to translate the zettel
  (`--language`/`-l`). The original zettel will not be overwritten, but the changed version will be appended to the original version.

- `search`: Search for Zettels using sematic search

- `scrape`: Scrape a web page and generate a new zettel which includes a summary of
  the web page.

- `tags`: This group allows you to work with tags. Not all commands in this
  group use AI.

  - `find-similar`: Use semantic search to find similar tags. It will compare
    all tags to all tags, and outputs the most similar tag pairs.
  - `list`: list all tags
  - `replace`:       Replace a tag with another tag in all zettels.
  - `sync`:          Sync tags in tagsfile with PyZettel's tags database


## Command reference

```bash
Usage: pyzettel ai [OPTIONS] COMMAND [ARGS]...

  AI commands group

Options:
  --help  Show this message and exit.

Commands:
  create   Create a new zettel
  improve  Improve an existing zettel using AI
  scrape   Scrape a web page at URL.
  search   Perform semantic search, using 'SEARCH_STRING'
  tags
```

```bash
Usage: pyzettel ai improve [OPTIONS]

  Improve an existing zettel using AI

Options:
  -z, --zettel-id TEXT  ID of the zettel  [required]
  -l, --language TEXT   Language for the generated article
  -r, --regards TEXT    Specify in which respects to improve. Can be given
                        multiple times.
  --help                Show this message and exit.
```

```bash
Usage: pyzettel ai scrape [OPTIONS] URL

  Scrape a web page at URL.

Options:
  -f, --file TEXT  File containing HTML to scrape
  -g, --tag TEXT   Tags for the zettel. Will be added to the auto generated
                   tags.
  --help           Show this message and exit.
```

```bash
Usage: pyzettel ai search [OPTIONS] SEARCH_STRING

  Perform semantic search, using 'SEARCH_STRING'

Options:
  --help  Show this message and exit.
```

```bash
Usage: pyzettel ai tags [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  find-similar
  list
  replace       Replace a tag with another tag in all zettels.
  sync          Sync tags in tagsfile with PyZettel's tags database
```

```bash
Usage: pyzettel ai tags list [OPTIONS]

Options:
  -r, --regexp TEXT               List tags matching this regex.
  -s, --show-zettel-title / -S, --no-show-zettel-title
                                  show zettels which have the tag.
  -i, --show-zettel-id / -I, --no-show-zettel-id
                                  show IDs of tagged zettels
  --help                          Show this message and exit.
```

```bash
Usage: pyzettel ai tags sync [OPTIONS]

  Sync tags in tagsfile with PyZettel's tags database

Options:
  --help  Show this message and exit.
```

```bash
Usage: pyzettel ai tags find-similar [OPTIONS]

Options:
  -s, --similarity-cutoff FLOAT  Cutoff for similarity
  --help                         Show this message and exit.
```

```bash
Usage: pyzettel ai tags replace [OPTIONS] TAG_SPEC

  Replace a tag with another tag in all zettels. TAG_SPEC is in the format
  <tag_to_replace>:<tag_replacement>

Options:
  --help  Show this message and exit.
```

```bash
Usage: pyzettel ai create [OPTIONS]

  Create a new zettel

Options:
  -t, --title TEXT             Title of the zettel  [required]
  -g, --tag TEXT               Tags for the zettel
  -l, --language TEXT          Language for the generated article
  -i, --additional-input TEXT  Additional input for AI
  --help                       Show this message and exit.
```