
```bash
Usage: pyzettel rag [OPTIONS] COMMAND [ARGS]...

  Retrieval augmented generation commands group

Options:
  --help  Show this message and exit.

Commands:
  ask      Ask your zettelkasten a question.
  init-db  Initialialize database used for RAG.
  update   Ask a question to the zettelkasten
```

```bash
Usage: pyzettel rag init-db [OPTIONS]

  Initialialize database used for RAG.

Options:
  --help  Show this message and exit.
```

```bash
Usage: pyzettel rag ask [OPTIONS] QUESTION

  Ask your zettelkasten a question.

Options:
  --llm-model TEXT                The model to use for the LLM
  -z, --show-used-zettels / -Z, --no-show-used-zettels
  -t, --show-used-tags / -T, --no-show-used-tags
  -m, --markdown / -M, --no-markdown
  --help                          Show this message and exit.
```

```bash
Usage: pyzettel rag update [OPTIONS]

  Ask a question to the zettelkasten

Options:
  --llm-model TEXT  The model to use for the LLM
  --help            Show this message and exit.
```

