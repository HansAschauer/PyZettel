import click
import platformdirs

from click_logging_config import LoggingConfiguration  # type: ignore


default_config_path = platformdirs.user_config_path("pyzettel")

config_file_option = click.option(
    "--config-file",
    "-c",
    default=default_config_path,
    help="Path to the configuration file",
)


# from https://stackoverflow.com/a/66743881
def common_options(fn):
    return click.option(
        "--config-file",
        "-c",
        default=default_config_path,
        help="Path to the configuration file",
    )(fn)


logging_config = LoggingConfiguration(
    log_level="info", enable_console_logging=True, enable_file_logging=False
)
