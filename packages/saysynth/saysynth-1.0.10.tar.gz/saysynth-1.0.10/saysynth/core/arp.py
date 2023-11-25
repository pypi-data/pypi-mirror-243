"""The Arp class enables melodic speech synthesis by mapping input text or phonemes onto a configurable arpeggiator.
<center><img src="/assets/img/cell.png"></img></center>
"""
import random
from functools import cached_property
from typing import List, Optional, Union

from midi_utils import midi_arp

from .base import SayObject
from .lyrics import Lyrics
from .note import Note
from .segment import Segment


class Arp(SayObject):
    def __init__(
        self,
        text: Optional[str] = None,
        notes: List[int] = [],
        root: str = "C2",
        chord: str = "min69",
        inversions: List[int] = [],
        stack: int = 0,
        styles: List[str] = ["down"],
        octaves: List[int] = [0],
        velocities: List[int] = [100],
        volume_level_per_note: int = 3,
        beat_bpm: float = 131.0,
        beat_count: Union[float, int, str] = "1/16",
        beat_time_sig: str = "4/4",
        beat_duration: Optional[float] = None,
        note_bpm: float = 131.0,
        note_count: Union[float, int, str] = "3/64",
        note_time_sig: str = "4/4",
        note_duration: Optional[float] = None,
        randomize_start: Optional[List[int]] = None,
        start_bpm: float = 131.0,
        start_count: Union[float, int, str] = 0,
        start_time_sig: str = "4/4",
        start_duration: Optional[float] = None,
        duration_bpm: float = 131.0,
        duration_count: Union[float, int, str] = "16",
        duration_time_sig: str = "4/4",
        duration: Optional[float] = None,
        loops: Optional[int] = None,
        **note_options,
    ):
        """
        Generate an arpeggiated melody

        Args:
            text: text to 'sing'
            notes: an arbitrary list of notes to arpeggiate
            root: root note of chord to arpeggiate
            chord: the chord name
            inversions: a list of inversions to apply to the chord notes
            stack: Stack a chord up (1) or down (-1)
            styles: A list of arpeggiated style names.
                    See https://gitlab.com/gltd/midi-utils/-/blob/main/midi_utils/arp.py for the full list.
            octaves: A list of octaves to add to the notes (eg: [-1, 2])
            velocities: A list of velocities for each note of the arpeggiator.
                        If this list is shorter than the list of notes, a modulo
                        operator is user.
            volume_level_per_note: How many notes it takes to re-adjust the volume/velocity.
                                  This parameter exists because too many volume changes
                                  can cause sporadically audio to dropout.
            beat_bpm: The bpm to use when calculating the duration of each beat of the arp.
            beat_count: The count of one beat of the arp
            beat_time_sig: str = The time signature of the arp.
            beat_duration: The duration of the beat. If provided, this overrides
                           the other beat_* parameters.
            note_bpm: The bpm to use when calculating the duration of each note of the arp.
                      By default, this is the
            note_count: The count of one beat of the arp
            note_time_sig: str = The time signature of the arp.
            note_duration: The duration of the beat. If provided, this overrides
                           the other note_* parameters.
            randomize_start: Optional[List[int]] = None,
            start_bpm: bpm to use when determining the start of the arp. The start_* parameters
                       adds silence at the beginning of the arpeggiator. This is particularly
                       useful when creating sequences.
            start_count: The count of one beat of starting silence.
            start_time_sig: The time signature to use when calculating the duration
                           of one beat of starting silence.
            start_duration: The amount of silence to add at the beginning in ms
            duration_bpm: bpm to use when determining the duration of the arpeggiator.
            duration_count: The duration beat count
            duration_time_sig: Time signature to use when determining duration
            duration: The total duration of the pattern in ms.
            loops: The number of times to loop the pattern.
                   This overrides `duration_*` settings.
            **note_options: Additional options to pass to `Note`.
                          These will affect how each note of the
                          arpeggiator sounds.

        """
        self.styles = styles

        if randomize_start:
            start_duration = random.choice(
                range(randomize_start[0], randomize_start[1] + 1)
            )

        self.sequence = midi_arp(
            notes=notes,
            root=root,
            chord=chord,
            inversions=inversions,
            stack=stack,
            octaves=octaves,
            styles=styles,
            velocities=velocities,
            beat_bpm=beat_bpm,
            beat_count=beat_count,
            beat_time_sig=beat_time_sig,
            beat_duration=beat_duration,
            note_bpm=note_bpm,
            note_count=note_count,
            note_time_sig=note_time_sig,
            note_duration=note_duration,
            start_bpm=start_bpm,
            start_count=start_count,
            start_time_sig=start_time_sig,
            start_duration=start_duration,
            duration_bpm=duration_bpm,
            duration_count=duration_count,
            duration_time_sig=duration_time_sig,
            duration=duration,
            loops=loops,
        )
        self.volume_level_per_note = volume_level_per_note
        self._note_options = note_options
        self.lyrics = None
        if text:
            # HACK: add padding to prevent skipping phonemes
            # TODO: figure why this is happening.
            self.lyrics = Lyrics(" . " + text + " . ")

    def _get_kwargs(self, index, **kwargs):
        """
        get kwargs + update with new ones
        used for mapping similar kwargs over different notes
        """
        d = dict(self._note_options.items())
        d.update(kwargs)
        d["include_volume_level"] = index % self.volume_level_per_note == 0
        return d

    @cached_property
    def notes(self) -> List[Note]:
        """
        The generated list of `Note` in the Arp.
        """
        start_at_phoneme = 0
        _notes = []
        for i, note in enumerate(self.sequence):
            note_kwargs = self._get_kwargs(i, **note)
            if self.lyrics:
                # handle text / phoneme:
                phonemes = self.lyrics.get_phonemes(start_at=start_at_phoneme)
                if len(phonemes) == 0:
                    # TODO: Fix this hack.
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

    def to_text(self):
        """
        Render this Arp as Apple SpeechSynthesis DSL text.
        """
        return "\n".join([n.to_text() for n in self.notes])

    def __repr__(self):
        return f"<Arp {','.join(self.styles)} {','.join(str(n) for n in self.notes)}>"
