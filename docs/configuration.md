# PyZettel Configuration

PyZettel has two main configuration files:

- `pyzettel_plugins`: This file is located at `<config-dir>/pyzettel_plugins`,
    unless the `PYZETTEL_PLUGIN_CONFIG` environment variable is set to a
    different value. `config-dir` depends on the operating system. See the
    platformdir
    documentation](https://platformdirs.readthedocs.io/en/latest/api.html#user-config-directory)
    for details.

    Note that it is not possible to set this configuration file on the command
    line, since plugins change the command line parser -- so they must be
    configured before the command line parser is set up.

- `pyzettel`: This file is located at `<config-dir>/pyzettel`, unless the
  `--config-file` option is given on the command line.

## `pyzettel_plugins`

```yaml
plugins:
  pyzettel.plugins.ai:
  pyzettel.plugins.hello:
  pyzettel.plugins.rag:
    api_name: "google"
    api_key: "google-cloud api key"
    api_key_keyword: "google_api_key"
    additional_embedder_init_options:
      model: "models/embedding-001"    
loader_config:
  log_level: WARNING
```

## `pyzettel`

```yaml
id_template: '{{now | hexdate(12)}}'
zettelkasten_proj_dir: /home/hans/zettelkasten
zettelkasten_subdir: docs
editor: code
editor_args: []
ai_options:
    base_url: https://generativelanguage.googleapis.com/v1beta/openai/
    api_key: "google-cloud api key"
    engine: gemini-2.0-flash-lite
    embeddings_engine: text-embedding-004
```