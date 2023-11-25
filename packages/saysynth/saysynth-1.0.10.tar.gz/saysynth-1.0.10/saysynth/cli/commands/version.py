"""
Print the current version of `saysynth` to the console.
"""
import click

from saysynth.cli.colors import blue, green, red, yellow
from saysynth.version import VERSION


@click.command()
def cli():
    """
    Print the current version of `saysynth` to the console.
    """
    click.echo(
        f"➡️ {green('saysynth')} ({red('sy')}) {yellow('version:')} {blue(VERSION)}",
        err=True,
    )
