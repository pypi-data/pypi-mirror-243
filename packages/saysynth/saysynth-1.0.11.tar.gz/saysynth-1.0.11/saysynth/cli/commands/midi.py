"""
Synthesize a melody from a monophonic midi file.
"""

import os

import click

from saysynth.cli.options import (adsr_opts, group_options, log_configurations,
                                  phoneme_opts, randomize_velocity_opt,
                                  say_opts, segment_opts, start_opts, text_opt,
                                  velocity_emphasis_opt, volume_level_opts,
                                  volume_range_opt)
from saysynth.constants import DEFAULT_SEQUENCE_NAME
from saysynth.core import MidiTrack, controller


def run(**kwargs):
    midi_track = MidiTrack(**kwargs)
    midi_track.cli(**kwargs)


@click.command()
@click.argument("midi_file", required=True)
@click.option(
    "-l",
    "--loops",
    default=1,
    show_default=True,
    type=int,
    help="The number of times to loop the midi file",
)
@start_opts
@phoneme_opts
@text_opt
@group_options(velocity_emphasis_opt, volume_range_opt, randomize_velocity_opt)
@volume_level_opts
@adsr_opts
@segment_opts
@click.option(
    "-o",
    "--output-file",
    type=str,
    help="A filepath to write the generated text to",
)
@say_opts
def cli(**kwargs):
    """
    Synthesize a melody from a fully-monophonic midi file.
    """
    if kwargs["yaml"]:
        return log_configurations("midi", **kwargs)
    parent_pid = os.getpid()
    ad = kwargs.get("audio_device", "")
    controller.add_parent_pid(DEFAULT_SEQUENCE_NAME, "midi", ad, parent_pid)
    kwargs["parent_pid"] = parent_pid
    return run(**kwargs)
