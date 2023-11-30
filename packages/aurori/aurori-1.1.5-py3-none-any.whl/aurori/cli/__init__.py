import click

from . import core

@click.group()
def client():
    pass

client.add_command(core.core)

if __name__ == '__main__':
    client()