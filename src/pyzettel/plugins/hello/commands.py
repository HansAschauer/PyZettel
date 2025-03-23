import click

config = {}
def set_config(conf:dict):
    global config
    config = conf
@click.group()
def dummy():
    "Dummy plugin, used to demonstrate plugin system"
    pass

@dummy.command()
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(name):
    click.echo(f"Enabled: {config['enabled']}")
    click.echo(f"options: {config['options']}")
    click.echo(f"Hello, {name}!")

@dummy.command()
@click.option("--name", prompt="Your name", help="The person to greet.")
def good_bye(name):
    click.echo(f"Enabled: {config['enabled']}")
    click.echo(f"options: {config['options']}")
    click.echo(f"Good bye, {name}!")
    
commands = [dummy]