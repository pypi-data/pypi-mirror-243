"""
Synthesize an arpeggiated melody.
"""
import click
from midi_utils import note_to_midi

from saysynth.cli.options import (adsr_opts, arp_opts, chord_opts,
                                  duration_opts, log_configurations,
                                  output_file_opt, phoneme_opts,
                                  randomize_velocity_opt, say_opts,
                                  segment_opts, start_opts, text_opt,
                                  velocity_emphasis_opt, volume_level_opts,
                                  volume_range_opt)
from saysynth.core import Arp, controller


def run(**kwargs):
    """
    Generate an arpeggiated melody.
    """
    arp = Arp(**kwargs)
    arp.cli(**kwargs)


@click.command()
@click.argument("root", type=note_to_midi, default="A2")
@arp_opts
@chord_opts
@velocity_emphasis_opt
@volume_range_opt
@randomize_velocity_opt
@volume_level_opts
@start_opts
@duration_opts
@phoneme_opts
@text_opt
@segment_opts
@adsr_opts
@output_file_opt
@say_opts
def cli(**kwargs):
    """
    Generate an arpeggiated melody.
    """
    if kwargs["yaml"]:
        return log_configurations("arp", **kwargs)
    kwargs = controller.handle_cli_options("arp", **kwargs)
    return run(**kwargs)
