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
  pyzettel.plugins.hello:
    enabled: true
    options:
      dummy_option: dummy_value
  pyzettel.plugins.rag:
    enabled: true
    options:
      chroma_data_dir: /home/hans/.local/share/pyzettel-ask

  pyzettel.plugins.ai:
    enabled: true
  pyzettel.plugins.google_genai:
    enabled: false
    options:
      api_key: GOOGLE-CLOUD-api-key
      llm_model: gemini-2.0-flash-lite
      embeddings_model: text-embedding-004
  pyzettel.plugins.openai:
    enabled: true
    options:
      api_key: OPENAI-API-key
      # base_url: https://api.example.org/llm/
      embeddings_model: text-embedding-ada-002
      llm_model: gpt-3.5-turbo

loader_config:
  log_level: WARNING```

## `pyzettel`

```yaml
editor: code
editor_args: []
id_template: '{{now | hexdate(12)}}'
zettelkasten_proj_dir: /home/hans/zettelkasten/
zettelkasten_subdir: docs
opencitations_api_key: 
```