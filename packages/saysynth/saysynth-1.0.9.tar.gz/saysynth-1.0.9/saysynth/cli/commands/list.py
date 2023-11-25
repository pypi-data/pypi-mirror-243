"""
List all currently running `saysynth` processes.
"""
import click

from saysynth.cli.colors import blue, green, red, yellow
from saysynth.core import controller


def run(**kwargs):
    pids = controller.list_pids()
    if not len(pids):
        click.echo(red("There are no active processes!"))
        return
    last_seq = None
    for p in pids:
        seq = p["seq"]
        if last_seq != seq:
            click.echo(r"-" * 79, err=True)
            click.echo(f"{red('sequence')}: {green(seq)}")
            click.echo(r"-" * 79, err=True)
        click.echo(
            f"➡️ {yellow('track')}: {blue(p['track']).ljust(23)} {yellow('audio_device')}: {blue(p['ad']).ljust(18)} {yellow('parent_pid')}: {blue(p['parent_pid']).ljust(14)} {yellow('child_pids')}: {blue(len(p['child_pids']))}"
        )
        last_seq = seq


@click.command()
def cli(**kwargs):
    """
    List all currently running `saysynth` processes.
    """
    run(**kwargs)
