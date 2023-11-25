"""
The `saysynth.cli.options` module includes shared `click.option` instances for use throughout all commands.

<center><img src="/assets/img/sun-wavy.png"></img></center>

**NOTE**: The documentation for this module is not rendered properly by `pdoc`, so its best to  click "View Source" to scan its contents.
"""
import types
from collections import defaultdict
from typing import Any, Dict, List, Union

import click
import yaml
from midi_utils.arp import STYLES
from midi_utils.constants import CHORDS

from saysynth.constants import (DEFAULT_BPM_TIME_BPM, DEFAULT_BPM_TIME_COUNT,
                                DEFAULT_BPM_TIME_SIG, SAY_ALL_PHONEMES,
                                SAY_DATA_TYPES, SAY_EMPHASIS, SAY_ENDIANNESS,
                                SAY_EXTRA_OPTION_DELIMITER,
                                SAY_PHONEME_CLASSES, SAY_SEGMENT_MAX_DURATION,
                                SAY_TUNED_VOICES, SAY_VOLUME_LEVEL_PER_NOTE,
                                SAY_VOLUME_LEVEL_PER_SEGMENT, SAY_VOLUME_RANGE)
from saysynth.utils import random_track_name, update_dict


def group_options(*options):
    def wrapper(function):
        for option in reversed(options):
            function = option(function)
        return function

    return wrapper


def csv_list(csv: str) -> List[str]:
    """
    A parser for a csv option
    """
    return [v.strip() for v in csv.split(",") if v.strip()]


def csv_int_list(csv: str) -> List[int]:
    """
    A parser for an integer-typed csv option
    """
    return [int(v) for v in csv_list(csv)]


def prepare_options_for_say(input_text: str, **kwargs):
    """
    TODO: Get rid fo this / move to `saysynth.lib.say`?
    """
    # handle some param edge cases
    rp = kwargs.get("randomize_phoneme")
    # for convenience, set the voice option to the one specified
    # in randomize phoneme.
    if rp and ":" in rp:
        kwargs["voice"] = rp.split(":")[0].strip().title()
    kwargs["input_text"] = input_text
    return kwargs


def format_opt_value(name: str, value: Any) -> Any:
    """
    Format an option value given its name and value.
    If the name is part of the common `OPTS`
    set, the click-configured type function will
    be applied, otherwise the value will be returned
    as a string.
    """
    global OPTS
    name = expand_opt_name(name)
    if name in OPTS:
        return OPTS[name]["obj"].type(value)
    return str(value).strip()


def _standardize_opt_name(opt_name: str) -> str:
    """
    Strip leading dashes from a cli option.
    """
    opt_name = opt_name.strip()
    while True:
        if opt_name[0] == "-":
            opt_name = opt_name[1:]
        else:
            break
    return opt_name.lower().replace("-", "_")


def shorten_opt_name(opt_name: str) -> str:
    """
    If an option is present in `OPTS`, return its short_name, otherwise standardize it.
    """
    o = _standardize_opt_name(opt_name)
    return OPTS.get(o, {}).get("short_name", o)


def expand_opt_name(opt_name: str) -> str:
    """
    Strip leading dashes from an option name, lower case and strip.
    and then expand any shortened / non-canonical opts with the global `OPTS` set.
    """
    o = _standardize_opt_name(opt_name)
    return OPTS.get(o, {}).get("full_name", o)


def get_unspecified_opts(
    context: click.Context,
) -> Dict[str, Union[Dict[str, Any], Any]]:
    """
    Get unspecified options from the click.Context and parse their
    accompanying values using the global `OPTS` set.
    """
    opts = {}
    try:
        for i in range(0, len(context.args), 2):
            raw_cli_opt_name = context.args[i]
            raw_cli_opt_val = context.args[i + 1]
            if SAY_EXTRA_OPTION_DELIMITER in raw_cli_opt_name:
                # handle options which are designed to be nested (eg: tracks in a sequence for config_overrides)
                parent_opt_name, child_opt_name = raw_cli_opt_val.split(
                    SAY_EXTRA_OPTION_DELIMITER
                )
                parent_opt_name = _standardize_opt_name(parent_opt_name)
                child_opt_name = expand_opt_name(child_opt_name)
                if parent_opt_name not in opts:
                    opts[parent_opt_name] = {}
                opts[parent_opt_name][child_opt_name] = format_opt_value(
                    child_opt_name, raw_cli_opt_val
                )
            else:
                cli_opt_name = expand_opt_name(raw_cli_opt_name)
                opts[cli_opt_name] = format_opt_value(
                    cli_opt_name, raw_cli_opt_val
                )
    except IndexError:
        pass
    return opts


def set_config_overrides_opt(
    context: click.Context, **kwargs
) -> Dict[str, Any]:
    """
    Combine the config overrides option and additional, unspecified cli options
    """
    cli_config_overrides = get_unspecified_opts(context)
    yaml_config_overrides = yaml.safe_load(
        kwargs.get("config_overrides", "{}")
    )
    kwargs["config_overrides"] = update_dict(
        cli_config_overrides, yaml_config_overrides
    )
    return kwargs


def log_configurations(track_type, **options) -> Dict[str, Any]:
    """
    Log configurations as yaml and exit
    """
    track_name = random_track_name(track_type, **options)
    options.pop("yaml", None)  # remove yaml option
    configs = {"tracks": [{track_name: {"type": track_type, "options": options}}]}
    click.echo(yaml.safe_dump(configs, indent=4))
    return configs


# Duration Options


duration_opt = click.option(
    "-d",
    "--duration",
    default=10000,
    type=int,
    help="The duration of the note in milliseconds.",
)

bpm_opt = click.option(
    "-db",
    "--duration-bpm",
    "duration_bpm",
    default=DEFAULT_BPM_TIME_BPM,
    show_default=True,
    type=float,
    help="The bpm to use when calculating note duration.",
)
count_opt = click.option(
    "-dc",
    "--duration-count",
    "duration_count",
    default=DEFAULT_BPM_TIME_COUNT,
    type=str,
    show_default=True,
    help="The note length to use when calculating note duration (eg: 1/8 or 0.123 or 3)",
)
time_sig_opt = click.option(
    "-dts",
    "--duration-time-sig",
    "duration_time_sig",
    default=DEFAULT_BPM_TIME_SIG,
    type=str,
    show_default=True,
    help="The time signature to use when calculating note duration",
)

"""
CLI options for controlling note duration.
"""
duration_opts = group_options(duration_opt, bpm_opt, count_opt, time_sig_opt)


phoneme_opt = click.option(
    "-ph",
    "--phoneme",
    default="m",
    help=(
        f"One or more valid phoneme to use. Choose from {', '.join(SAY_ALL_PHONEMES)}. "
        "Multiple phonemes can be combined together into one option eg: ''"
    ),
    show_default=True,
    type=csv_list,
)
randomize_phoneme_opt = click.option(
    "-rp",
    "--randomize-phoneme",
    show_default=True,
    type=str,
    help=(
        "Randomize the phoneme for every note. "
        "If `all` is passed, all phonemes will be used. "
        "Alternatively pass a comma-separated list of phonemes (eg 'm,l,n') or a voice and style, eg: Fred:drone. "
        f"Valid voices include: {', '.join(SAY_TUNED_VOICES)}. "
        f"Valid styles include: {', '.join(SAY_PHONEME_CLASSES)}."
    ),
)
randomize_octave_opt = click.option(
    "-ro",
    "--randomize-octave",
    type=csv_int_list,
    required=False,
    default="",
    help="A comma-separate list of octaves to randomly vary between. You can weight certain octaves by providing them multiple times (eg: 0,0,0-1,-1,2 would prefer the root octave first, one octave down second, and two octaves up third.)",
)

"""
CLI options for controlling phonemes.
"""
phoneme_opts = group_options(
    phoneme_opt, randomize_phoneme_opt, randomize_octave_opt
)


# Start Options


randomize_start_opt = click.option(
    "-rt",
    "--randomize-start",
    type=int,
    nargs=2,
    help="Randomize the number of milliseconds to silence to add before the say text. The first number passed in is the minimum of the range, the second is the max.",
)
start_opt = click.option(
    "-t",
    "--start",
    default=None,
    show_default=True,
    type=float,
    help="The number of milliseconds of silence to add before the say text.",
)
start_bpm_opt = click.option(
    "-tb",
    "--start-bpm",
    default=DEFAULT_BPM_TIME_BPM,
    type=float,
    help="The bpm to use when calculating start time",
)
start_count_opt = click.option(
    "-tc",
    "--start-count",
    default=0,
    type=str,
    show_default=True,
    help="The note length to use when calculating start time (eg: 1/8 or 0.123 or 3)",
)
start_time_sig_opt = click.option(
    "-tts",
    "--start-time-sig",
    default=DEFAULT_BPM_TIME_SIG,
    type=str,
    show_default=True,
    help="The time signature to use when calculating start time",
)

"""
CLI options for adding silence to the beginning of a musical passage.
"""
start_opts = group_options(
    randomize_start_opt,
    start_opt,
    start_bpm_opt,
    start_count_opt,
    start_time_sig_opt,
)


# Segment Options

randomize_segments_opt = click.option(
    "-rs",
    "--randomize-segments",
    type=csv_list,
    required=False,
    default="",
    help="Randomize every segment's 'phoneme', 'octave', and/or 'velocity'. Use commas to separate multiple randomization strategies",
)


segment_duration_opt = click.option(
    "-sd",
    "--segment-duration",
    default=SAY_SEGMENT_MAX_DURATION,
    show_default=True,
    type=float,
    help="The duration an individual phoneme",
)
segment_bpm_opt = click.option(
    "-sb",
    "--segment-bpm",
    default=120.0,
    show_default=True,
    type=float,
    help="The bpm to use when calculating phoneme duration",
)
segment_count_opt = click.option(
    "-sc",
    "--segment-count",
    default="1/16",
    type=str,
    show_default=True,
    help="The note length to use when calculating phoneme duration (eg: 1/8 or 0.123 or 3)",
)
segment_time_sig_opt = click.option(
    "-sts",
    "--segment-time-sig",
    default=DEFAULT_BPM_TIME_SIG,
    type=str,
    show_default=True,
    help="The time signature to use when calculating phoneme duration",
)

"""
CLI options for controlling segment generation.
"""
segment_opts = group_options(
    randomize_segments_opt,
    segment_duration_opt,
    segment_bpm_opt,
    segment_count_opt,
    segment_time_sig_opt,
)


# Velocity Options

velocity_opt = click.option(
    "-vl",
    "--velocity",
    type=int,
    show_default=True,
    default=110,
    help="The midi velocity value to use for each note.",
)
velocity_emphasis_opt = click.option(
    "-ve",
    "--velocity-emphasis",
    "emphasis",
    type=int,
    nargs=2,
    show_default=True,
    default=SAY_EMPHASIS,
    help="Two midi velocity values (between 0 and 127) at which to add emphasis to a note/segment",
)
volume_range_opt = click.option(
    "-vr",
    "--volume-range",
    type=float,
    nargs=2,
    show_default=True,
    default=SAY_VOLUME_RANGE,
    help="The min and max volumes (range: 0.0-1.0) to use when mapping from midi velocities",
)
randomize_velocity_opt = click.option(
    "-rv",
    "--randomize-velocity",
    type=int,
    nargs=2,
    help="Randomize a note's velocity by supplying a min and max midi velocity (eg: -rv 40 120)",
)

"""
CLI options for controlling velocities
"""
velocity_opts = group_options(
    velocity_opt,
    velocity_emphasis_opt,
    volume_range_opt,
    randomize_velocity_opt,
)


volume_level_per_segment_opt = click.option(
    "-vps",
    "--render-volume-level-per-segment",
    "volume_level_per_segment",
    default=SAY_VOLUME_LEVEL_PER_SEGMENT,
    type=int,
    show_default=True,
    help="The number of segments per note to render volume tags. Rendering too many can cause random drop-outs, while too few decreases the granularity of ADSR settings.",
)

volume_level_per_note_opt = click.option(
    "-vpn",
    "--render-volume-level-per-note",
    "volume_level_per_note",
    default=SAY_VOLUME_LEVEL_PER_NOTE,
    type=int,
    show_default=True,
    help="The number of notes per sequence to render volume tags. Rendering too many can cause random drop-outs, while too few decreases the granularity of ADSR settings.",
)

"""
CLI options for adjusting the granularity of volume envelopes.
"""
volume_level_opts = group_options(
    volume_level_per_note_opt, volume_level_per_segment_opt
)


attack_opt = click.option(
    "-at",
    "--attack",
    default=0.0,
    show_default=True,
    type=float,
    help="The percentage of the duration it takes to reach the max volume of the note",
)
decay_opt = click.option(
    "-de",
    "--decay",
    default=0.0,
    show_default=True,
    type=float,
    help="The percentage of the duration it takes to reach the sustain volume of the note",
)
sustain_opt = click.option(
    "-su",
    "--sustain",
    default=1.0,
    type=float,
    show_default=True,
    help="The the sustain volume of the note",
)
release_opt = click.option(
    "-re",
    "--release",
    default=0.0,
    type=float,
    show_default=True,
    help="The percentage of the duration it takes to reach the min volume of the note",
)

"""
CLI options for ADSR functionality.
"""
adsr_opts = group_options(
    attack_opt,
    decay_opt,
    sustain_opt,
    release_opt,
)


# Say Options
exec_opt = click.option(
    "-p",
    "--pipe",
    is_flag=True,
    default=False,
    help=(
        "Don't execute the say command and print the text to the console instead. "
        "NOTE: This doesn't work with the `chord` command since this launches "
        "multiple subprocesses and the outputted text will be jumbled. "
        "In order to output the text representation of a chord, use "
        "the `--output-file` option."
    ),
)

rate_opt = click.option(
    "-r",
    "--rate",
    type=int,
    default=70,
    show_default=True,
    help="Rate to speak at (see `man say`)",
)
voice_opt = click.option(
    "-v",
    "--voice",
    type=click.Choice(SAY_TUNED_VOICES),
    default="Fred",
    show_default=True,
    help="Voice to use",
)
input_file_opt = click.option(
    "-i",
    "--input-file",
    type=str,
    help="Filepath to read text input for say from",
    default=None,
)
audio_output_file_opt = click.option(
    "-ao",
    "--audio-output-file",
    type=str,
    help="File to write audio output to",
)
audio_device_opt = click.option(
    "-ad",
    "--audio-device",
    type=str,
    help="Name of the audio device to send the signal to",
)
networks_send_opt = click.option(
    "-ns",
    "--network-send",
    type=str,
    help="Network address to send the signal to",
)
stereo_opt = click.option(
    "-st",
    "--stereo",
    is_flag=True,
    default=False,
    help="Whether or not to generate a stereo signal",
)
endianness_opt = click.option(
    "-en",
    "--endianness",
    type=click.Choice(SAY_ENDIANNESS),
    default="BE",
    help="Whether or not to generate a stereo signal. See say's documentation on data/file formats for more details.",
)
data_type_opt = click.option(
    "-dt",
    "--data-type",
    type=click.Choice(SAY_DATA_TYPES),
    default="I",
    help="One of F (float), I (integer), or, rarely, UI (unsigned integer). See say's documentation on data/file formats for more details.",
)
sample_size_opt = click.option(
    "-ss",
    "--sample-size",
    type=int,
    default=16,
    show_default=True,
    help="Sample size of the signal. When --data-type is 'I', One of 8, 16, 24, 32, 64. When --data-type is 'F', either 32 or 64. See say's documentation on data/file formats for more details.",
)
sample_rate_opt = click.option(
    "-sr",
    "--sample-rate",
    type=int,
    default=22050,
    show_default=True,
    help="Sample rate of the signal (0:22050). See say's documentation on data/file formats for more details.",
)
quality_opt = click.option(
    "-qu",
    "--quality",
    type=int,
    default=127,
    help="Quality of the signal (1:127). See say's documentation on data/file formats for more details.",
    show_default=True,
)
wait_opt = click.option(
    "-w",
    "--wait",
    is_flag=True,
    default=False,
    help="Whether or not to wait for the process to complete.",
)
yaml_opt = click.option(
    "-y",
    "--yaml",
    is_flag=True,
    default=False,
    help="Optionally print these configurations to the console as yaml. This is useful when constructing a sequence.",
)
# progress_bar_opt = click.option(
#     "-pg",
#     "--progress",
#     is_flag=True,
#     default=False,
#     help="Whether or not to display an interactive progress bar",
# )
# interactive_opt = click.option(
#     "-in",
#     "--interactive",
#     is_flag=True,
#     default=False,
#     help="Whether or not to display highlighted text",
# )
# text_color_opt = click.option(
#     "-cf",
#     "--text-color",
#     type=click.Choice(SAY_COLORS),
#     default="white",
#     help="The text color to use when displaying highlighted text",
# )
# bg_color_opt = click.option(
#     "-cb",
#     "--bg-color",
#     type=click.Choice(SAY_COLORS),
#     default="black",
#     help="The background color to use when displaying highlighted text",
# )

output_file_opt = click.option(
    "-o",
    "--output-file",
    type=str,
    help="A filepath to write the generated text to",
)

"""
CLI options for `say`
"""
say_opts = group_options(
    exec_opt,
    wait_opt,
    rate_opt,
    voice_opt,
    audio_output_file_opt,
    audio_device_opt,
    networks_send_opt,
    stereo_opt,
    endianness_opt,
    data_type_opt,
    sample_size_opt,
    sample_rate_opt,
    quality_opt,
    yaml_opt,
    # progress_bar_opt,
    # interactive_opt,
    # text_color_opt,
    # bg_color_opt,
)


# Chord Options

chord_opt = click.option(
    "-c",
    "--chord",
    required=False,
    default="min69",
    type=click.Choice([c.lower() for c in CHORDS.keys()]),
    help="An optional name of a chord to build using the note as root.",
)
chord_notes_opt = click.option(
    "-cn",
    "--chord-notes",
    required=False,
    default="",
    type=csv_int_list,
    help="An optional list of midi numbers to build a chord from based off of the root. For example, the notes '0,3,7' with the root of 'C1' would create a C-minor chord.",
)
chord_velocities_opt = click.option(
    "-cv",
    "--chord-velocities",
    required=False,
    type=csv_int_list,
    help="A comma-separated list of integers (eg: '50,100,127') specifying the midi velocity each note i the chord. The length of this list much match the number of notes in the chord. --volume-range and --velocity-steps also modify this parameter",
)
chord_inversions_opt = click.option(
    "-ci",
    "--chord-inversions",
    "inversions",
    default="",
    required=False,
    type=csv_int_list,
    help="A comma-separated list of integers (eg: '0,1,-1') specifying the direction and amplitude to invert each note. The length of this list much match the number of notes in the chord (post-stack).",
)
chord_stack_opt = click.option(
    "-cs",
    "--chord-stack",
    "stack",
    default=0,
    required=False,
    type=int,
    help="Stack a chord up (eg: '1' or '2') or down (eg: '-1' or '-2').",
)

"""
CLI options for handling chords (`sy arp` + `sy chord`)
"""
chord_opts = group_options(
    chord_opt,
    chord_notes_opt,
    chord_inversions_opt,
    chord_stack_opt,
)

# Arp Options

#
notes_opt = click.option(
    "-ns",
    "--notes",
    required=False,
    default="",
    type=csv_list,
    help="A comma-separated list of note names / midi note numbers to argpeggiate",
)

octaves_opt = click.option(
    "-oc",
    "--octaves",
    required=False,
    default="0",
    type=csv_int_list,
    help="A comma-separated list of octaves to add to the notes",
)

styles_opt = click.option(
    "-sl",
    "--styles",
    required=False,
    default="down",
    type=csv_list,
    help=f"A comma-separated list of styles/sorting algorithms to apply to the notes. This occurs after octaves are added. \nchoose from:\n {', '.join([str(k) for k in STYLES.keys()])}",
)

velocities_opt = click.option(
    "-vl",
    "--velocities",
    required=False,
    default="100",
    show_default=True,
    type=csv_int_list,
    help="A comma-separated list of velocities to apply to the notes, if this list is shorter than the list of notes, a modulo lookup is performed.",
)

loops_opt = click.option(
    "-l",
    "--loops",
    default=None,
    show_default=True,
    type=int,
    help="The number of times to loop the notes in the pattern. If this is set, it will override the '--duration' option.",
)

## beat duration

beat_duration_opt = click.option(
    "-bd",
    "--beat-duration",
    default=None,
    required=False,
    type=int,
    help="The duration of the beat in milliseconds.",
)
beat_bpm_opt = click.option(
    "-bb",
    "--beat-bpm",
    default=DEFAULT_BPM_TIME_BPM,
    type=float,
    show_default=True,
    help="The bpm to use when calculating beat duration.",
)
beat_count_opt = click.option(
    "-bc",
    "--beat-count",
    default=DEFAULT_BPM_TIME_COUNT,
    type=str,
    show_default=True,
    help="The note count to use when calculating beat duration (eg: 1/8 or 0.123 or 3)",
)
beat_time_sig_opt = click.option(
    "-bts",
    "--beat-time-sig",
    default=DEFAULT_BPM_TIME_SIG,
    type=str,
    show_default=True,
    help="The time signature to use when calculating beat duration",
)


note_duration_opt = click.option(
    "-nd",
    "--note-duration",
    default=None,
    required=False,
    type=int,
    help="The duration of a single note in the arp. Defaults to the beat duration",
)
note_bpm_opt = click.option(
    "-nb",
    "--note-bpm",
    "note_bpm",
    default=DEFAULT_BPM_TIME_BPM,
    type=float,
    show_default=True,
    help="The bpm to use when calculating note duration.",
)
note_count_opt = click.option(
    "-nc",
    "--note-count",
    "note_count",
    default=DEFAULT_BPM_TIME_COUNT,
    type=str,
    show_default=True,
    help="The note length to use when calculating note duration (eg: 1/8 or 0.123 or 3)",
)
note_time_sig_opt = click.option(
    "-nts",
    "--note-time-sig",
    default=DEFAULT_BPM_TIME_SIG,
    type=str,
    show_default=True,
    help="The time signature to use when calculating note duration",
)

"""
CLI options specific to `sy arp`.
"""
arp_opts = group_options(
    notes_opt,
    octaves_opt,
    styles_opt,
    velocities_opt,
    loops_opt,
    beat_duration_opt,
    beat_bpm_opt,
    beat_count_opt,
    beat_time_sig_opt,
    note_duration_opt,
    note_bpm_opt,
    note_count_opt,
    note_time_sig_opt,
)

seq_tracks_opt = click.option(
    "-t",
    "--tracks",
    type=csv_list,
    help="A comma-separated list of track names to `play`, `start`, `stop`, or `render`",
)
seq_audio_devices_opt = click.option(
    "-ad",
    "--audio-devices",
    type=csv_list,
    help="A comma-separated list of audio-devices  to `play`, `start`, `stop`, or `render`",
)
seq_output_dir_opt = click.option(
    "-o",
    "--output-dir",
    type=str,
    default="./",
    help="When using `render`, the directory to write audio files of sequence's individual tracks into.",
)
seq_config_overrides_opt = click.option(
    "-c",
    "--config-overrides",
    type=str,
    default="{}",
    help="""
    Override global and track-level configurations at runtime
    by passing in yaml-formatted configurations,
    eg: `-c '{"foo":"bar"}'`.
    These configurations can be specified at the track-level
    by nesting them under the track name,
    eg: `-c '{"track":{"foo":"bar"}}'`.

    You can also override configurations by providing extra command line arguments
    available to `midi`, `note`, `chord`, rand/or `arp` tracks, eg: `-sd 10` or `--segment-duration 10`.
    These can be similarly nested by using a `__` separator, eg: `--track__segment-duration 10`.
    Parameters specified via the --config-overrides option will
    take precedence over any extra CLI arguments.
    """,
)
seq_command_arg = click.argument(
    "command",
    type=click.Choice(["play", "start", "stop", "render", "echo"]),
    required=True,
)

"""
CLI options specific to `sy seq` and `sy demo`.
"""
seq_opts = group_options(
    seq_tracks_opt,
    seq_audio_devices_opt,
    seq_output_dir_opt,
    seq_config_overrides_opt,
)

"""
Text to to use when selecting phonemes; the text to 'sing'
"""
text_opt = click.option(
    "-tx",
    "--text",
    type=str,
    default=None,
    help="Text to to use when selecting phonemes; the text to 'sing'. Can also be a path to a file containing text to sing.",
)


def _build_option_set(locals) -> Dict[str, click.Parameter]:
    """
    Meta-programming HACK to build an option set we can use to dynamically
    parse extra cli options.
    """
    click_params = defaultdict(dict)
    for _, object in locals.items():
        if not (
            isinstance(object, types.FunctionType)
            and object.__module__.startswith("click")
        ):
            continue
        # instantiate this option and fetch its param object
        param: click.Parameter = object(lambda x: x).__click_params__[0]
        full_name = _standardize_opt_name(param.name)
        option = {"obj": param, "full_name": full_name}
        click_params[param.name] = option

        # also add lookup for short name flags
        short_cli_opt = [
            o
            for o in param.opts
            if o.startswith("-") and not o.startswith("--")
        ]
        if not len(short_cli_opt):
            continue

        # add lookup to short name
        short_name = _standardize_opt_name(short_cli_opt[0])
        click_params[param.name]["short_name"] = short_name
        # also add reverse lookup
        click_params[short_name] = option
        click_params[short_name]["short_name"] = short_name
    return click_params


OPTS: Dict[str, click.Parameter] = _build_option_set(locals())
