# PyZettel CLI

All `pyzettel` commands allow to set two generic options:

* `--config-file`/`-c`: Configuration file path. If not provided, use `<config-dir>/pyzettel`. `config-dir` depends on the operating system. See the [platformdir documentation](https://platformdirs.readthedocs.io/en/latest/api.html#user-config-directory) for details.
* `--log-level`/`-l`: log level

Generic options must be passed before the command.

The following commands are available:


-   **[ai](ai.md)**        AI commands group. Provided by the `ai` builtin plugin
-   **[create](create.md)**    Create a new zettel
-   **[init](init.md)**      Initialize a new pyzettel configuration
-   **[list](list.md)**      List zettels, using GLOB as a search pattern.
-   **[paper](paper.md)**     Create a zettel from a paper DOI
-   **[rag](rag.md)**       Retrieval augmented generation commands group.
    Provided by the `rag` builtin plugin
-   **[rm](rm.md)**        Delete a zettel
-   **[show](show.md)**      Show a zettel on the command line or in an editor.
-   **[dumphelp](other.md)**  Show all CLI commands and options
-   **[dummy](other.md)**     Dummy plugin, used to demonstrate plugin system.
    Provided by the `hello` builtin plugin



```bash
Usage: pyzettel [OPTIONS] COMMAND [ARGS]...

  pyzettel command line interface

Options:
  -c, --config-file TEXT          Path to the configuration file
  -l, --log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Set logging level
  --help                          Show this message and exit.

Commands:
  ai        AI commands group
  create    Create a new zettel
  dummy     Dummy plugin, used to demonstrate plugin system
  dumphelp  Show all CLI commands and options
  init      Initialize a new pyzettel configuration
  list      List zettels, using GLOB as a search pattern.
  paper     Create a zettel from a paper DOI
  rag       Retrieval augmented generation commands group
  rm        Delete a zettel
  show      Show a zettel on the command line or in an editor.
```