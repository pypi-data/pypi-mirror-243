"""
Play a sequence of `chord`, `midi`, `note`, and/or `arp` tracks via yaml configuration.
"""

import copy
import os
from argparse import ArgumentError
from multiprocessing.pool import ThreadPool as Pool
from typing import Dict

import click
import yaml

from saysynth.cli.colors import blue, green, red, yellow
from saysynth.cli.commands import arp, chord, midi, note
from saysynth.cli.options import (expand_opt_name, seq_command_arg, seq_opts,
                                  set_config_overrides_opt)
from saysynth.core import controller
from saysynth.utils import calculate_total_duration


def run(**kwargs):
    controller.ensure_pid_log()

    # process configurations
    config_path = kwargs.pop("base_config")
    command = kwargs.pop("command")
    output_dir = kwargs.pop("output_dir", "./")
    if config_path:
        # print config
        if command == "echo":
            click.echo(str(config_path.read()))
            return
        base_config = yaml.safe_load(config_path)
    else:
        base_config = {"name": "*"}

    globals = base_config.pop("globals", {})
    seq = base_config.pop("name", None)
    if seq is None:
        raise ArgumentError("You must set a `name` in your sequence config")

    tracks = kwargs.get("tracks", None) or []
    audio_devices = kwargs.get("audio_devices", None) or []

    # log sequence name
    click.echo("-" * 79, err=True)
    click.echo(f"{red('sequence')}: {yellow(seq)}", err=True)
    click.echo("-" * 79, err=True)

    # play/start sequences/tracks
    if command in ["play", "start", "render"]:
        track_configs = []
        for track, base_track_config in base_config.get("tracks", {}).items():

            # optionally skip tracks
            if len(tracks) and track not in tracks:
                continue

            # allow for track-specific overrides
            config_overrides = kwargs.get("config_overrides", {})
            track_overrides = config_overrides.pop(track, {})
            config_overrides.update(track_overrides)

            # create track config
            track_options = copy.copy(globals)  # start with globals
            base_track_options = {
                expand_opt_name(k): v
                for k, v in base_track_config.get("options", {}).items()
            }  # expand the names of shortened sequence options
            track_options.update(base_track_options)
            track_options.update(config_overrides)

            # optionally filter by audio device
            ad = track_options.get("audio_device", None)
            if len(audio_devices) and ad not in audio_devices:
                continue

            # optionally start tracks immediately
            if command == "start":
                track_options["start_count"] = 0

            # optionally render tracks
            if command == "render":
                try:
                    os.makedirs(output_dir)
                except FileExistsError:
                    pass
                track_options["audio_output_file"] = os.path.join(
                    output_dir,
                    f"{seq}-{track}-{base_track_config['type']}.aiff",
                )

            # construct track configs
            base_track_config["options"] = track_options
            track_configs.append((seq, track, ad, base_track_config, command))

        # run everything
        for _ in Pool(len(track_configs)).imap(run_track_func, track_configs):
            continue

    if command == "stop":

        if len(audio_devices):
            for ad in audio_devices:
                click.echo(
                    f"🛑 {red('stopping')} ➡️ all tracks on  {yellow('audio_device')}: {blue(ad)}",
                    err=True,
                )
                controller.stop_child_pids(seq, track=None, ad=ad)

        else:
            if not len(tracks):
                tracks = ["*"]
            for track in tracks:
                click.echo(
                    f"🛑 {red('stopping')} ➡️ {yellow('track')}: { blue(track)}",
                    err=True,
                )
                controller.stop_child_pids(seq, track)


TRACK_FUNCS: Dict[str, callable] = {
    "chord": chord.run,
    "midi": midi.run,
    "note": note.run,
    "arp": arp.run,
}


def run_track_func(item):
    seq_name, track, ad, kwargs, command = item
    pid = os.getpid()
    parent_pid_file = controller.add_parent_pid(seq_name, track, ad, pid)
    type = kwargs.get("type", None)
    options = kwargs.get("options", {})
    options["parent_pid"] = pid  # pass parent id to child process.
    options["parent_pid_file"] = parent_pid_file

    if type not in TRACK_FUNCS:
        raise ValueError(
            f'Invalid track type: {type}. Choose from: {",".join(TRACK_FUNCS.keys())}'
        )
    colorfx = green
    if command == "stop":
        colorfx = red

    # calculate total_duration of track
    total_duration = calculate_total_duration(**options)

    click.echo(
        f"▶️ {colorfx(f'{command}ing')} ➡️ {yellow('track')}: {blue(track).ljust(25)} {yellow('audio_device')}: {blue(ad or 'default').ljust(20)} {yellow('parent_pid')}: {blue(pid).ljust(15)} {yellow('total_duration')}: {blue(total_duration)}",
        err=True,
    )
    return TRACK_FUNCS.get(type)(**options)


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@seq_command_arg
@click.argument("base_config", type=click.File(), required=False)
@seq_opts
@click.pass_context
def cli(context, **kwargs):
    """
    Play a sequence of `chord`, `midi`, `note`, and/or `arp` tracks
    via yaml configuration.

    BASE_CONFIG is a path to a yaml file.

    COMMAND can be:

        play: Plays the sequence as specified in the config file

        start Starts all tracks in the sequence, irregardless of their "start" times.

        stop: Stop tracks in the sequence.

        render: Writes out individual aiff/wav files for each track in the sequence.

        echo: Pretty print the sequence config to the console.

    """
    run(**set_config_overrides_opt(context, **kwargs))
