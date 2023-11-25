"""
Synthesize a polyphonic chord.
"""
import click
from midi_utils import note_to_midi

from saysynth.cli.options import (adsr_opts, chord_opts, duration_opts,
                                  log_configurations, phoneme_opts, say_opts,
                                  segment_opts, start_opts, text_opt,
                                  velocity_opts, volume_level_opts)
from saysynth.core import Chord, controller


def run(**kwargs):
    """
    Given a note name (or midi note number), stream text required to generate a continuous drone for input to say
    """
    # generate chord
    chord = Chord(**kwargs)
    chord.cli(**kwargs)


@click.command()
@click.argument("root", type=note_to_midi, default="A2")
@text_opt
@chord_opts
@start_opts
@duration_opts
@velocity_opts
@volume_level_opts
@adsr_opts
@phoneme_opts
@segment_opts
@click.option(
    "-o",
    "--output-file",
    type=str,
    help="A filepath to write the generated text to. This filepath will be used as a pattern to generate multiple text files, one per note in the chord.",
)
@say_opts
def cli(**kwargs):
    """
    Generate a polyphonic chord.
    """
    if kwargs["yaml"]:
        return log_configurations("chord", **kwargs)
    kwargs = controller.handle_cli_options("chord", **kwargs)
    return run(**kwargs)
