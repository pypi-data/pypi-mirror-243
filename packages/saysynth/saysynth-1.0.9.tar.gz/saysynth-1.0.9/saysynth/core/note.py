"""
The Note class creates a list of `Segment` with configurable
duration, pitch, phonemes, and volume envelope.
<center><img src="/assets/img/coffee.png"></img></center>
"""
import copy
import random
from typing import Any, Dict, List, Optional, Tuple, Union

from midi_utils import ADSR, midi_to_note, note_to_midi

from ..constants import (SAY_ALL_PHONEMES, SAY_PHONEME_CLASSES,
                         SAY_PHONEME_VOICE_CLASSES, SAY_SEGMENT_MAX_DURATION,
                         SAY_SEGMENT_SILENCE_DURATION, SAY_TUNED_VOICES)
from ..utils import bpm_to_time, frange
from .base import SayObject
from .lyrics import Lyrics
from .segment import Segment


class Note(SayObject):
    def __init__(
        self,
        note: Union[int, str] = "A3",
        phoneme: List[str] = ["m"],
        text: Optional[str] = None,
        # start position
        start: Optional[int] = 0,
        start_bpm: Optional[Union[float, int]] = 120,
        start_count: Union[str, float, int] = 0,
        start_time_sig: str = "4/4",
        # envelope
        velocity: int = 127,
        volume_level_per_segment: int = 3,
        include_volume_level: bool = True,
        attack: Union[float, int] = 0,
        decay: Union[float, int] = 0,
        sustain: Union[float, int] = 1,
        release: Union[float, int] = 0,
        # length
        duration: Optional[Union[float, int]] = None,
        duration_bpm: Optional[Union[float, int]] = 120,
        duration_count: Union[str, float, int] = 1,
        duration_time_sig: str = "4/4",
        # segmentation
        segment_duration: Optional[int] = None,
        segment_bpm: Optional[float] = 120,
        segment_count: Optional[Union[str, float, int]] = 1.0 / 8.0,
        segment_time_sig: Optional[str] = "4/4",
        # randomization
        randomize_phoneme: Optional[str] = None,
        randomize_velocity: Optional[Tuple[int, int]] = None,
        randomize_octave: Optional[List[int]] = [],
        randomize_segments: Optional[List[str]] = [],
        randomize_start: Optional[Tuple[int, int]] = None,
        **segment_options,
    ):
        f"""
        Generate say text for a collection of phonemes with adsr, pitch modulation, and more.
        Args:
            note: The note to play, eg "A3"
            phoneme: A valid combination of Phonemes documented in [Apple's Speech Synthesis guide](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/Phonemes/Phonemes.html#//apple_ref/doc/uid/TP40004365-CH9-SW1).
            text: The text to "sing". If provided, this will override phoneme.
            start: The number of milliseconds of silence to add to the beginning of the track.
            start_bpm: A BPM to use when calculating the number of milliseconds of silence to add to the beginning of the track.
            start_count: A count to use when calculating the number of milliseconds of silence to add to the beginning of the track.
            start_time_sig: A time signature to use when calculating the number of milliseconds of silence to add to the beginning of the track.
            velocity: The midi velocity value to use for this note (0-127).
            volume_level_per_segment: The number of segments after which volume settings will be rendered (eg: "3" would mean one segment would have volume settings and then the next two would not, etc.))
            include_volume_level: Whether or not to the render the volume settings for this note.
                         Over-rendering these settings can lead to audio drop-outs.
            attack: A value between 0 and 1 representing the ratio of the note's total length during which the note will increase to it's amplitude.
                    A lower number is a faster attack while a larger number is a slow attack. (see `midi_utils.ADSR`).
            decay:  A value between 0 and 1 representing the ratio of note's total length during which the note will decrease in amplitude from the max amplitude to the sustain level. (see `midi_utils.ADSR`).
            sustain: A value between 0 and 1 representing the relative volume level of the sustain phase (0 is the min volume_range, 1 is the max).
            release: A value between 0 and 1 representing the ratio of the note's total length during which the note will decrease in amplitude from the sustain level to zero.
            duration: The duration of this note in number of milliseconds.
            duration_bpm: A BPM to use when calculating the note's duration.
            duration_count: A count to use when calculating the note's duration.
            duration_time_sig: A time signature to use when calculating the note's duration.
            segment_duration: The duration of each `Segment` of this note in number of milliseconds.
            segment_bpm: A BPM to use when calculating the duration of each `Segment` in this note.
            segment_count: A count to use when calculating duration of each `Segment` of this note
            segment_time_sig: A time signature to use when calculating the duration of each `Segment` in this note.
            randomize_phoneme: Randomize the phoneme for every note. "
                If "all" is passed, all valid phonemes will be used.
                Alternatively pass a list of phonemes (eg 'm,l,n') or a voice and style, eg: Fred:drone.
                Valid voices include: {', '.join(SAY_TUNED_VOICES)}.
                Valid styles include: {', '.join(SAY_PHONEME_CLASSES)}.
            randomize_velocity: Randomize a note's velocity by supplying a min and max midi velocity (eg: -rv [40, 120])
            randomize_octave: A list of octaves to randomly vary between.
                              You can weight certain octaves by providing them multiple times
                              (eg: [0,0-1,-1,2] would prefer the root octave first, one octave down second, and two octaves up third).
            randomize_segments: Randomize the 'phoneme', 'octave', and/or 'velocity' according to each respective randomization setting.
            randomize_start: Randomize the number of milliseconds to silence to add before the say text.
                             The first number passed in is the minimum of the range, the second is the max (eg: [4000, 12000] would set a range for four to twelve seconds).
            **segment_options: Additional options to pass to each `Segment`.
        """

        self.segment_options = segment_options
        root = segment_options.pop("root", None)

        if root or note:
            self.note = note_to_midi(root or note)  # root == note
            self.name = midi_to_note(self.note)
        else:
            self.note = 0
            self.name = "silence"

        # phoneme
        self.phoneme = phoneme
        if isinstance(self.phoneme, str):
            self.phoneme = [phoneme]

        # text / lyrics
        self.lyrics = None
        if text:
            self.lyrics = Lyrics(text)

        # start position
        self.start = start
        if not self.start:
            self.start = bpm_to_time(start_bpm, start_count, start_time_sig)
        if randomize_start:
            self.start = random.choice(
                range(self.randomize_start[0], self.randomize_start[1] + 1)
            )

        # duration
        self.duration = duration
        if not self.duration:
            self.duration = bpm_to_time(
                duration_bpm, duration_count, duration_time_sig
            )

        # velocity
        self.velocity = velocity
        self.volume_level_per_segment = volume_level_per_segment
        self.include_volume_level = include_volume_level

        # segmentation
        self.segment_duration = segment_duration
        if not self.segment_duration:
            self.segment_duration = bpm_to_time(
                segment_bpm, segment_count, segment_time_sig
            )
        self.segment_duration = min(
            SAY_SEGMENT_MAX_DURATION, self.segment_duration
        )
        self.segment_count = int(self.duration / self.segment_duration) + 1

        # adsr
        self.adsr = ADSR(
            attack, decay, sustain, release, samples=self.segment_count
        )

        # randomization
        self.randomize_phoneme = randomize_phoneme
        self.randomize_velocity = randomize_velocity
        self.randomize_octave = randomize_octave
        self.randomize_segments = randomize_segments
        self.randomize_start = randomize_start

    def _get_random_phoneme(self, index: int) -> str:
        if self.randomize_phoneme == "all":
            return random.choice(SAY_ALL_PHONEMES)
        elif ":" in self.randomize_phoneme:
            voice, style = self.randomize_phoneme.split(":")
            voice = voice.title()  # allow for lowercase
            try:
                return random.choice(SAY_PHONEME_VOICE_CLASSES[voice][style])
            except KeyError:
                raise ValueError(
                    f"Invalid `voice` '{voice}' or `style` '{style}'. "
                    f"`voice` must be one of: {', '.join(SAY_TUNED_VOICES)}. "
                    f"`style` must be one of: {', '.join(SAY_PHONEME_CLASSES)}"
                )
        else:
            return random.choice(
                [c.strip() for c in self.randomize_phoneme.split(",")]
            )

    def _get_phoneme(self, index: int) -> str:
        # handle phoneme randomization
        if self.randomize_phoneme:
            return self._get_random_phoneme(index)

        if self.lyrics:
            return self.lyrics.get_phoneme_for_index(index)

        return self.phoneme[index % len(self.phoneme)]

    def _get_note(self) -> int:
        if len(self.randomize_octave):
            return (random.choice(self.randomize_octave) * 12) + note_to_midi(
                self.note
            )
        return self.note

    def _get_velocity(self) -> int:
        if self.randomize_velocity:
            return random.choice(
                range(
                    self.randomize_velocity[0], self.randomize_velocity[1] + 1
                )
            )
        return self.velocity

    def _get_segment_kwargs(self, **kwargs) -> Dict[str, Any]:
        opts = copy.copy(self.segment_options)
        opts.update(kwargs)
        return opts

    def _randomize_segment(self, note, velocity):

        # optionally randomize every segment.
        if "octave" in self.randomize_segments and self.randomize_octave:
            note = self._get_note()
        if "velocity" in self.randomize_segments and self.randomize_velocity:
            velocity = self._get_velocity()
        return note, velocity

    def _get_segment(
        self,
        index: int = 0,
        note: str = None,
        velocity: int = 0,
        duration: Optional[float] = None,
        **kwargs,
    ) -> Segment:
        """
        Generate each segment of the Note, applying randomization, ADSR settings, phoneme generation, and other Segment parameters.
        """
        note, velocity = self._randomize_segment(note, velocity)
        return Segment(
            note=note,
            velocity=velocity * self.adsr.get_value(index),
            phoneme=self._get_phoneme(index),
            duration=duration or self.segment_duration,
            include_volume_level=self.include_volume_level
            and index % self.volume_level_per_segment == 0,
            **self._get_segment_kwargs(**kwargs),
        )

    @property
    def segments(self) -> List[Segment]:
        """
        The generated list of `Segment` within the note.
        """
        _segments = []
        # get initial value of note + velocity + phoneme
        note = self._get_note()
        velocity = self._get_velocity()

        if self.start and self.start > 0:
            # create multiple silent phonemes which add up to the desired start position
            start_breaks = list(
                frange(0.0, self.start, SAY_SEGMENT_SILENCE_DURATION, 10)
            )
            for index, total_start_time in enumerate(start_breaks[1:]):
                segment = self._get_segment(index, type="silence", velocity=0)
                _segments.append(segment)

            if total_start_time < self.start:
                # add final step of silence
                _segments.append(
                    self._get_segment(index + 1, type="silence", velocity=0)
                )

        # create multiple phonemes which add up to the phoneme_duration
        segment_breaks = list(
            frange(0.0, self.duration, self.segment_duration, 10)
        )
        total_time = 0
        index = 0
        for index, total_time in enumerate(segment_breaks[1:]):
            segment = self._get_segment(
                index,
                note,
                velocity,
                type=self.segment_options.get("type", "note"),
            )
            _segments.append(segment)

        if total_time < self.duration and len(_segments) < self.segment_count:

            # add final step
            _segments.append(
                self._get_segment(
                    index + 1,
                    note,
                    velocity,
                    duration=self.duration - total_time,
                    type=self.segment_options.get("type", "note"),
                )
            )
        return _segments

    @property
    def n_segments(self):
        """
        The number of Segments in the Note.
        """
        return len(self.segments)

    def to_text(self) -> str:
        """
        Render this Note as Apple SpeechSynthesis DSL text.
        """
        return "\n".join([s.to_text() for s in self.segments])
