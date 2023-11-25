"""
Given a scale and other parameters, generate a sound-font of each note as an .aiff or .wav file.
"""
import click
from midi_utils import ROOT_TO_MIDI, SCALES

from saysynth.cli.options import (adsr_opts, duration_opts, phoneme_opts,
                                  say_opts, segment_opts, text_opt,
                                  velocity_opts, volume_level_opts)
from saysynth.core import Font


def run(**kwargs):
    font = Font(**kwargs)
    font.play(**kwargs)


@click.command()
@click.option(
    "-cs",
    "--scale-start-at",
    type=str,
    default="C3",
    help="Note name/number to start at",
)
@click.option(
    "-ce",
    "--scale-end-at",
    type=str,
    default="G5",
    show_default=True,
    help="Note name/number to end at",
)
@click.option(
    "-c",
    "--scale",
    type=click.Choice([s.lower() for s in SCALES]),
    default="minor",
    show_default=True,
    help="Scale name to use",
)
@click.option(
    "-k",
    "--key",
    type=click.Choice(ROOT_TO_MIDI.keys()),
    default="C",
    show_default=True,
    help="Root note of scale",
)
@click.option(
    "-od",
    "--output-dir",
    default="./",
    type=str,
    show_default=True,
    help="Directory to write to",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["wav", "aiff"]),
    default="aiff",
    show_default=True,
    help="Format of each note's file.",
)
@duration_opts
@phoneme_opts
@text_opt
@velocity_opts
@volume_level_opts
@adsr_opts
@segment_opts
@say_opts
def cli(**kwargs):
    """
    Given a scale and other parameters, generate a soundfont
    of each note as an .aiff or .wav file.
    """
    return run(**kwargs)
