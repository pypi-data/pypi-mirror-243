"""
A `Segment` is the base unit text according to
[Apple's Speech Synthesis Programming Guide](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/SpeechOverview/SpeechOverview.html#//apple_ref/doc/uid/TP40004365-CH3-SW1).
A segment represents an individual part-of-speech (phoneme) in `say` and can have
one or more phonemes, a duration, and a sequences of pitches.

Segments are combined together throughout `saysynth` to create musical passages.

<center><img src="/assets/img/cell.png"></img></center>

"""
from typing import Tuple, Union

from midi_utils import midi_to_freq, note_to_midi

from ..constants import (SAY_EMPHASIS, SAY_PHONEME_SILENCE,
                         SAY_SEGMENT_MAX_DURATION, SAY_VOLUME_RANGE)
from ..utils import rescale


class Segment(object):
    def __init__(
        self,
        note: Union[int, str],
        velocity: int = 127,
        phoneme: str = "m",
        duration: Union[float, int] = SAY_SEGMENT_MAX_DURATION,
        type: str = "note",
        emphasis: Tuple[int, int] = SAY_EMPHASIS,
        volume_range: Tuple[float, float] = SAY_VOLUME_RANGE,
        include_volume_level: bool = True,
        duration_sig_digits: int = 4,
        **kwargs,
    ):
        """
        An individual segment of speech in Apple's DSL
        Args:
            note: The note to map to a frequency, eg "A3"
            velocity: The midi velocity value to use for the segment (0-127).
            phoneme:  A valid combination of Phonemes documented in [Apple's Speech Synthesis guide](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/Phonemes/Phonemes.html#//apple_ref/doc/uid/TP40004365-CH9-SW1).
            duration: The duration of the segment in milliseconds.
            type: Either "note" or "silence"
            emphasis: A level of emphasis to place on this segment (0,1, or 2)
            volume_range: A range between 0 and 127 representing the minimum and maximum velocity values to render.
            include_volume_level: Whether or not to the render the volume settings for this segment.
                         Over-rendering these settings can lead to audio drop-outs.
            duration_sig_digits: The number of significant digits to use when rendering the duration value.
                                 A higher value should yield more rhythmically precise results.
        """
        self._phoneme = phoneme
        self._duration = duration
        self._emphasis = emphasis
        self.velocity = velocity
        self.note = note
        self.is_silence = type == "silence"
        self.volume_range = volume_range
        self.include_volume_level = include_volume_level
        self.duration_sig_digits = duration_sig_digits

    @property
    def phoneme(self):
        return self._phoneme

    @property
    def phoneme_has_emphasis(self) -> bool:
        """
        Return True if the `phoneme` has an included
        emphasis.
        """
        if (
            self._phoneme.startswith("0")
            or self._phoneme.startswith("1")
            or self._phoneme.startswith("2")
        ):
            return True
        return False

    @property
    def frequency_envelope(self) -> str:
        """
        Translate a note name to a frequency.
        **TODO:** Add intra-note modulation.
        """
        freq = midi_to_freq(note_to_midi(self.note))
        return f"P {freq}:0"

    @property
    def duration(self) -> float:
        """
        Clamp segment duration at `SAY_SEGMENT_MAX_DURATION`
        and round it to `self.duration_sig_digits`
        """
        return round(
            min(self._duration, SAY_SEGMENT_MAX_DURATION),
            self.duration_sig_digits,
        )

    @property
    def volume(self) -> str:
        """
        Translate a midi velocity value (0-127) into a pair
        of say volume tags, eg: "[[ volm +0.1 ]]"
        """
        if self.include_volume_level:
            volume = rescale(self.velocity, [0, 127], self.volume_range)
            return f"[[ volm {volume} ]]"
        return ""

    @property
    def emphasis(self) -> str:
        """
        Translate a midi velocity value (0-127) into a phoneme
        emphasis value ("", "1", or "2")when provided with a tuple
        of steps (step_1, step_2) eg: (75, 100)
        This action is not performed when the phoneme already
        has an emphasis included.
        """
        if not self.phoneme_has_emphasis:
            if not self.velocity:
                return ""
            if self.velocity > self._emphasis[1]:
                return "2"
            if self.velocity > self._emphasis[0]:
                return "1"
        return ""

    def to_text(self) -> str:
        """
        Render this Segment as Apple SpeechSynthesis DSL text.
        """
        if self.is_silence:
            return f"{self.volume} {SAY_PHONEME_SILENCE} {{D {self.duration}}}"
        return f"{self.volume} {self.emphasis}{self.phoneme} {{D {self.duration}; {self.frequency_envelope}}}"

    def __eq__(self, other):
        return self.to_text() == other.to_text()

    def __str__(self) -> str:
        return self.to_text()
