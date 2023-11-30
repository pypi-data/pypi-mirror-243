import click

from aurori.version import version as aurori_version

@click.group()
def core():
    pass

@core.command()
def version():
    """Display the current version."""
    click.echo(aurori_version)