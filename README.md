
# PyZettel

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

`PyZettel` is a command-line interface tool designed to help you organize your [Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten) efficiently. With integrated AI features, PyZettel automates tasks like generating summaries from web pages, performing similarity searches for content and tags, and providing interactive capabilities to engage with your Zettelkasten via a retrieval-augmented generation pipeline. PyZettel is developed in Python and offers a robust plugin system, making it versatile for various use cases.

## Documentation

Documentation is available on [github-pages](https://hansaschauer.github.io/PyZettel/).

## Features

- Create and manage Zettels with ease.
- AI-powered capabilities for improved content management.
- Generate Zettels from academic papers using DOIs.
- Perform semantic searches and content similarity operations.
- Interactive questioning with the Zettelkasten using RAG (Retrieval Augmented Generation).
- Plugin system for extending functionality.
- Intuitive CLI for fast and efficient navigation.

## Installation

### Development version from github

In order to install PyZettel, clone it from [github](https://github.com/HansAschauer/PyZettel):
```bash
git clone git@github.com:HansAschauer/PyZettel.git
```

This version uses `uv` to manage dependencies etc. See the [`uv`
documentation](https://docs.astral.sh/uv/getting-started/installation/) for
installation instructions.

Download all dependencies using `uv sync --extra=ai --extra=ai-rag`.

Run `pyzettel` using `uv run pyzettel --help`.

## Usage

PyZettel provides various commands and options to manage your Zettelkasten. Below is a summary of the core commands:

### General

```bash
Usage: pyzettel [OPTIONS] COMMAND [ARGS]...

Options:
  -c, --config-file TEXT          Path to the configuration file
  -l, --log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Set logging level
  --help                          Show this message and exit.
```

### Commands

- **ai**: Group of AI-related commands.
- **create**: Command to create a new zettel.
- **dummy**: Demonstrates the plugin system.
- **dumphelp**: Displays help for all CLI commands and options.
- **init**: Initialize a new PyZettel configuration.
- **list**: Lists zettels using a pattern.
- **paper**: Create a zettel from a DOI.
- **rag**: Commands for retrieval-augmented generation functionalities.
- **rm**: Delete a zettel.
- **show**: Displays a zettel in CLI or editor.

### AI Commands

- **create**: Use AI to create a new zettel.
- **improve**: Enhance an existing zettel.
- **scrape**: Scrape a web page.
- **search**: Perform a semantic search.
- **tags**: Manage tags interactively.

### RAG Commands

- **ask**: Ask a question to your zettelkasten.
- **init-db**: Initialize database for RAG operations.
- **update**: Update interaction with your zettelkasten.

### Plugin System

PyZettel supports plugins for extending its capabilities. The `dummy` command is provided as a demonstration:

```bash
Usage: pyzettel dummy [OPTIONS] COMMAND [ARGS]...

Commands:
  good-bye
  hello
```

## Using LMM (AI)

In order to use the AI features, you  need API access to large language models (LLM) and embedding models. At this point in time, two APIs can be used through the plugin interface:

- [Open AI](https://platform.openai.com/docs/overview): The most prominent
  provider for this API is, of course, OpenAI. However, there are other LLMs
  which provide a compatible API. If you do not use Open AI, you have to set the `base_url` parameter in the [plugin configuration](https://hansaschauer.github.io/PyZettel/configuration/).

- [Google Gemini](https://aistudio.google.com/welcome): This API is mostly or exclusively used by Google Gemini.

### API tokens and paid subscriptions
For most API providers, an API key is required. Many providers have free tiers
which might be ok for testing this software. For serious usage, in many cases a
payed subscription will lead to more satisfying results, since free tiers are
often rate limited.

During development, I used a Goggle Gemini account, and the cumulative costs
during the first several weeks were less than 0.05€.


## Contributing

Contributions are welcome! Please submit a pull request or open an issue for feedback.

## License

PyZettel is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

