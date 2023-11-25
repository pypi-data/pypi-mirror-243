"""
Stop currently running `saysynth` processes by `sequences`, `tracks`, `audio_devices`, and/or `parent_pids`
"""
import click

from saysynth.cli.colors import blue, red, yellow
from saysynth.core import controller


@click.command()
@click.option(
    "-p",
    "--pids",
    "parent_pid",
    type=lambda x: [int(t.strip()) for t in x.split(",") if t.strip()],
    help="Stop currently running `saysynth` processes by passing in the `parent_pids`",
    default=None,
)
@click.option(
    "-s",
    "--sequences",
    "seq",
    type=lambda x: [t.strip() for t in x.split(",") if t.strip()],
    help="Stop currently running `saysynth` processes by passing in the `sequence ` names",
    default=None,
)
@click.option(
    "-ad",
    "--audio-devices",
    "ad",
    type=lambda x: [t.strip() for t in x.split(",") if t.strip()],
    help="Stop currently running `saysynth` processes by passing in the `audio_devices`",
    default=None,
)
@click.option(
    "-t",
    "--tracks",
    "track",
    type=lambda x: [t.strip() for t in x.split(",") if t.strip()],
    help="Stop currently running `saysynth` processes by passing in the `track` names",
    default=None,
)
def cli(**kwargs):
    """
    Stop currently running `say` processes by `sequence`, `track`, `audio_device`, and/or `parent_pid`
    """
    all_null = True
    for key in ["seq", "track", "ad", "parent_pid"]:
        vals = kwargs.get(key, None)
        if not vals:
            continue
        all_null = False
        for val in vals:
            click.echo(f"🛑 {red('stopping')} ➡️ {yellow(key)}: {blue(val)}")
            controller.stop_child_pids(**{key: val})
            if key == "parent_pid":
                controller.rm_parent_pid(parent_pid=val)
    if all_null:
        click.echo(f"🛑 {red('stopping')} ➡️ {yellow('all processes')}!")
        controller.stop_child_pids()
