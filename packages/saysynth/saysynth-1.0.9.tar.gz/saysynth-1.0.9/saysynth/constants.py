"""
Constants for use throughout `saysynth`
"""
import os

SAY_EXECUTABLE = os.getenv("SAYSYNTH_SAY_EXECUTABLE", "/usr/bin/say")
"""The path to where the `say` command exists."""

SAY_FILE_FORMATS = ["wav", "aiff"]
"""Valid output file formats."""

SAY_TUNED_VOICES = ["Alex", "Fred", "Victoria"]
"""`say` voices which respect [[TUNE]] input"""

SAY_TUNE_TAG = "[[inpt TUNE]]"
"""Opening tag for tuned input to `say`"""

SAY_COLORS = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]
"""Colors which can used to style the interactive output of `say`"""

SAY_ENDIANNESS = ["BE", "LE"]
"""Values for --data-format to determine the endianness"""

SAY_DATA_TYPES = ["F", "I", "UI"]
"""Values for --data-format to determine the data type"""

SAY_SAMPLE_SIZES = [8, 16, 24, 32, 64]
"""Values for --data-format to determine the sample size"""

SAY_FILE_FORMATS = {
    "mp3": "mp4f",
    "aiff": "AIFF",
    "aif": "AIFF",
    "flac": "FLAC",
    "m4a": "m4af",
    "wav": "WAVE",
}
"""Mapping of file extension to say's --file-format arguments"""

SAY_BIG_ENDIAN_ONLY_FILE_FORMATS = ["AIFF", "m4af", "FLAC"]
"""List of say's --file-format arguments which accept only BE endianness"""

SAY_DEFAULT_FLOAT_SAMPLE_SIZE = 32
"""The default sample size to use when the data_type is F"""

SAY_VALID_FLOAT_SAMPLE_SIZES = [32, 64]
"""A list of valid sample sizes when the data_type is F"""

SAY_MAX_SAMPLE_RATE = 22050
"""
This is the max sample rate,
anything above this [will generate up-sampled audio](https://stackoverflow.com/questions/9729153/error-on-say-when-output-format-is-wave)
"""

SAY_ALL_PHONEMES = [
    "AE",
    "EY",
    "AO",
    "AX",
    "IY",
    "EH",
    "IH",
    "AY",
    "IX",
    "AA",
    "UW",
    "UH",
    "UX",
    "OW",
    "AW",
    "OY",
    "b",
    "C",
    "d",
    "D",
    "f",
    "g",
    "h",
    "J",
    "k",
    "l",
    "m",
    "n",
    "N",
    "p",
    "r",
    "s",
    "S",
    "t",
    "T",
    "v",
    "w",
    "y",
    "z",
    "Z",
]
"""
[A list of all valid phonemes to pass into `say`]( https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/Phonemes/Phonemes.html#//apple_ref/doc/uid/TP40004365-CH9-SW1).
"""

SAY_PHONEME_CLASSES = ["drone", "noise", "note"]
""" Classes of phonemes as defined in scripts/classify_phonemes.py """

SAY_PHONEME_VOICE_CLASSES = {
    "Alex": {
        "drone": [
            "AE",
            "EY",
            "AO",
            "AX",
            "IY",
            "EH",
            "IH",
            "AY",
            "IX",
            "UW",
            "OW",
            "OY",
            "h",
            "l",
            "m",
            "n",
            "N",
            "r",
            "Z",
        ],
        "noise": [
            "C",
            "d",
            "D",
            "f",
            "J",
            "k",
            "p",
            "s",
            "S",
            "t",
            "T",
            "v",
            "z",
            "Z",
        ],
        "note": ["AA", "UH", "UX", "AW", "b", "g", "w", "y", "Z"],
    },
    "Fred": {
        "drone": [
            "AE",
            "EY",
            "AO",
            "AX",
            "IY",
            "EH",
            "IH",
            "AY",
            "IX",
            "AA",
            "UW",
            "UH",
            "UX",
            "OW",
            "AW",
            "OY",
            "D",
            "l",
            "m",
            "n",
            "N",
            "r",
            "v",
            "w",
            "y",
            # "z",
            # "Z",
        ],
        "note": [  # all of Fred's drones work as notes.
            "AE",
            "EY",
            "AO",
            "AX",
            "IY",
            "EH",
            "IH",
            "AY",
            "IX",
            "AA",
            "UW",
            "UH",
            "UX",
            "OW",
            "AW",
            "OY",
            "D",
            "l",
            "m",
            "n",
            "N",
            "r",
            "v",
            "w",
            "y",
            "z",
            "Z",
        ],
        "noise": [
            "b",
            "C",
            "d",
            "f",
            "g",
            "h",
            "J",
            "k",
            "p",
            "s",
            "S",
            "t",
            "T",
        ],
    },
    "Victoria": {
        "drone": [
            "AE",
            "EY",
            "AO",
            "AX",
            "IY",
            "EH",
            "IH",
            "AY",
            "IX",
            "AA",
            "UW",
            "UH",
            "UX",
            "AW",
            "OY",
            "l",
            "m",
            "n",
            "N",
            "r",
            "v",
            "w",
            "y",
        ],
        "noise": [
            "C",
            "d",
            "D",
            "f",
            "h",
            "k",
            "p",
            "s",
            "S",
            "t",
            "T",
            "z",
            "Z",
        ],
        "note": ["OW", "b", "g", "J"],
    },
}
""" Generated by running scripts/classify_phonemes.py """

SAY_PHONEME_SILENCE = "%"
""" This is the sound of silence """

G2P_PHONEMES_TO_SAY_PHONEMES = {
    "AA0": "AA",
    "AA1": "1AA",
    "AA2": "2AA",
    "AE0": "AE",
    "AE1": "1AE",
    "AE2": "2AE",
    "AH0": "AAh",
    "AH1": "1AAh",
    "AH2": "2AAh",
    "AO0": "AO",
    "AO1": "1AO",
    "AO2": "2AO",
    "AW0": "AW",
    "AW1": "1AW",
    "AW2": "2AW",
    "AY0": "AY",
    "AY1": "1AY",
    "AY2": "2AY",
    "B": "b",
    "CH": "C",
    "D": "d",
    "DH": "T",
    "EH0": "EH",
    "EH1": "1EH",
    "EH2": "2EH",
    "ER0": "AXr",
    "ER1": "1AXr",
    "ER2": "2AXr",
    "EY0": "EY",
    "EY1": "1EY",
    "EY2": "2EY",
    "F": "f",
    "G": "g",
    "HH": "h",
    "IH0": "IH",
    "IH1": "1IH",
    "IH2": "2IH",
    "IY0": "IY",
    "IY1": "1IY",
    "IY2": "2IY",
    "JH": "J",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "N",
    "OW0": "OW",
    "OW1": "1OW",
    "OW2": "2OW",
    "OY0": "OY",
    "OY1": "1OY",
    "OY2": "2OY",
    "P": "p",
    "R": "r",
    "S": "s",
    "SH": "S",
    "T": "t",
    "TH": "T",
    "UH0": "UH",
    "UH1": "1UH",
    "UH2": "2UH",
    "UW": "UW",
    "UW0": "0UW",
    "UW1": "1UW",
    "UW2": "2UW",
    "V": "v",
    "W": "w",
    "Y": "y",
    "Z": "z",
    "ZH": "Z",
}
"""
A lookup between phonemes in [G2P](https://github.com/Kyubyong/g2p/blob/master/g2p_en/g2p.py#L55)
and [say](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/Phonemes/Phonemes.html#//apple_ref/doc/uid/TP40004365-CH9-SW1).
"""

SAY_SEGMENT_MAX_DURATION = 1200
"""
The number of milliseconds at which the duration
of an individual phoneme stops changing
"""

SAY_SEGMENT_SILENCE_DURATION = 1000
"""
This is the number of milliseconds to use for an individual segment of silence.
"""

SAY_EMPHASIS = [75, 100]
"""
The midi velocity values above which we add an emphasis to a phoneme.
"""

SAY_VOLUME_RANGE = [0.0, 1.0]
"""
The min and max range of volume levels to map to from midi velocities.
"""

SAY_VOLUME_LEVEL_PER_NOTE = 2
"""
The number of notes per sequence to show volume tags.
Including too many volume tags in a single command can cause random drop-outs.
"""

SAY_VOLUME_LEVEL_PER_SEGMENT = 4
"""
The number of segments per note to show volume tags.
Including too many volume tags in a single command can cause random drop-outs.
"""

DEFAULT_SEQUENCE_NAME = "sy"
"""
The sequence name to assign to a process when launched outside the context
of a sequence.
"""

DEFAULT_BPM_TIME_SIG = "4/4"
DEFAULT_BPM_TIME_BPM = 120
DEFAULT_BPM_TIME_COUNT = 1

SAY_EXTRA_OPTION_DELIMITER = "__"
