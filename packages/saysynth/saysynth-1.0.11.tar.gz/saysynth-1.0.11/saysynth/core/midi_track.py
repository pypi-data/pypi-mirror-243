"""
The MidiTrack class enables the translation notes in
a midi file into Apple's SpeechSynthesis DSL.
<center><img src="/assets/img/sun-wavy.png"></img></center>
"""
from typing import List, Optional, Union

from ..constants import SAY_SEGMENT_SILENCE_DURATION
from ..lib import midi
from ..utils import bpm_to_time, frange
from .base import SayObject
from .lyrics import Lyrics
from .note import Note
from .segment import Segment


class MidiTrack(SayObject):
    def __init__(
        self,
        midi_file: str,
        loops: int = 1,
        # start position
        start: Optional[int] = None,
        start_bpm: Optional[Union[float, int]] = 120,
        start_count: Union[str, float, int] = 0,
        start_time_sig: str = "4/4",
        text: Optional[str] = None,
        **kwargs,
    ):
        """
        Generate a melody from a monophonic midifile
        Args:
            midi_file: A path to the midi file
            loops: the number of times to loop the pattern in the midi file.
            # start position
            start: The number of milliseconds of silence to add to the beginning of the track.
            start_bpm: A BPM to use when calculating the number of milliseconds of silence to add to the beginning of the track.
            start_count: A count to use when calculating the number of milliseconds of silence to add to the beginning of the track.
            start_time_sig: A time signature to use when calculating the number of milliseconds of silence to add to the beginning of the track.
            text: The text to to "sing"
        **note_options: Additional options to pass to `Note`.
                        These will affect how each note of the
                        arpeggiator sounds.
        """
        self.midi_file = midi_file
        self.loops = loops

        self.start = start
        if not self.start:
            self.start = bpm_to_time(start_bpm, start_count, start_time_sig)
        self.start_segment_count = (
            int(self.start / SAY_SEGMENT_SILENCE_DURATION) + 1
        )
        self._note_options = kwargs
        self._start_segments = []
        # text / lyrics
        self.lyrics = None
        if text:
            # HACK: add padding to prevent skipping phonemes
            self.lyrics = Lyrics(" . " + text + " . ")

    @property
    def notes(self) -> List[Note]:
        """
        The generated list of `Note` in the MidiTrack.
        """
        _notes = []
        start_at_phoneme = 0
        last_note_length = 0
        for _ in range(0, self.loops):
            for note in midi.process(self.midi_file):
                note_kwargs = {**self._note_options, **note}
                # handle text / phoneme:
                if self.lyrics:
                    phonemes = self.lyrics.get_phonemes(
                        start_at=start_at_phoneme
                    )
                    if len(phonemes) == 0:
                        start_at_phoneme = 0
                        phonemes = self.lyrics.get_phonemes(
                            start_at=start_at_phoneme
                        )
                    note_kwargs["phoneme"] = phonemes
                note = Note(**note_kwargs)
                last_note_length = note.n_segments
                start_at_phoneme += last_note_length
                _notes.append(note)
        return _notes

    @property
    def segments(self) -> List[Segment]:
        """
        The generated list of `Segment` in the Arp.
        """
        return [segment for note in self.notes for segment in note.segments]

    @property
    def n_notes(self) -> int:
        """
        The number of Notes in the Arp.
        """
        return len(self.notes)

    @property
    def n_segments(self) -> int:
        """
        The number of Segments in the Arp.
        """
        return sum([note.n_segments for note in self.notes])

    @property
    def _start_text(self) -> str:
        """
        Add starting silence to the MidiTrack.
        """
        if not self.start:
            return ""
        _start_segments = []
        time_breaks = list(
            frange(0.0, self.start, SAY_SEGMENT_SILENCE_DURATION, 10)
        )[1:]
        for _, total_time in enumerate(time_breaks):
            _start_segments.append(
                Segment(
                    type="silence",
                    velocity=0,
                    duration=SAY_SEGMENT_SILENCE_DURATION,
                )
            )

        if (
            total_time < self.start
            and len(_start_segments) < self.start_segment_count
        ):
            # add final silent step
            dur = self.start - total_time
            _start_segments.append(
                Segment(type="silence", velocity=0, duration=dur)
            )
        return "\n".join(_start_segments)

    def to_text(self):
        """
        Render this MidiTrack as Apple SpeechSynthesis DSL text
        """
        note_texts = (n.to_text() for n in self.notes)
        return self._start_text + "\n" + "\n".join(note_texts)

    def __repr__(self):
        return f"<MidiTrack {self.midi_file}>"
