"""
The Chord class creates a list of `Note` which can be played in parallel, producing polyphonic sounds.
<center><img src="/assets/img/coffee.png"></img></center>
"""
from typing import Any, Dict, List

from midi_utils import midi_chord, note_to_midi

from ..cli.options import prepare_options_for_say
from ..lib import say
from .note import Note


class Chord(object):
    """
    The Chord class creates a list of `Note` objects which can
    be played in parallel, producing polyphonic sounds.

    Args:
        note/root: The base root of the chord
        chord_notes: An optional list of midi numbers to build a chord from based off of the root. For example, the notes '[0,3,7]' with the root of 'C1' would create a C-minor chord.
        **note_options: Additional options to pass to `Note`. These will affect how each note of the arpeggiator sounds.
    """

    def __init__(self, note=None, root=None, chord_notes=[], **note_options):
        self.root = note or root or "A1"  # root == note
        self.root_midi = note_to_midi(self.root)
        self.chord_notes = chord_notes
        self.note_options = note_options

    def _get_kwargs(self, **kwargs) -> Dict[str, Any]:
        """
        get kwargs + update with new ones
        used for mapping similar kwargs over different notes
        """
        d = dict(self.note_options.items())
        d.update(kwargs)
        return d

    @property
    def midi_notes(self) -> List[int]:
        # check for arbitrary notes
        if len(self.chord_notes):
            return [self.root_midi + n for n in self.chord_notes]
        return midi_chord(root=self.root, **self.note_options)

    @property
    def notes(self) -> List[Note]:
        """
        The generated list of `Note` in the Chord.
        """
        _notes = []
        for n in self.midi_notes:
            _notes.append(Note(**self._get_kwargs(note=n)))
        return _notes

    @property
    def n_notes(self) -> int:
        """
        The number of Notes in the Chord.
        """
        return len(self.notes)

    def write(self, output_file: str) -> None:
        """
        Write each Note in the Chord to an output file,
        adding the note name to the provided filepath.
        """
        for note in self.notes:
            fn = ".".join(output_file.split(".")[:-1])
            ext = (
                "txt" if "." not in output_file else output_file.split(".")[-1]
            )
            note_output_file = f"{fn}-{note.note}.{ext}"
            with open(note_output_file, "w") as f:
                f.write(note.to_say_text())

    def _get_audio_output_file_for_note(self, filename, note: Note) -> str:
        fn = ".".join(filename.split(".")[:-1])
        ext = "aiff" if "." not in filename else filename.split(".")[-1]
        return f"{fn}-{note.name}.{ext}"

    def _get_cmd_for_note(self, note: Note):
        cmd = prepare_options_for_say(
            input_text=note.to_say_text(),
            **self._get_kwargs(note=note.note, type="note"),
        )
        audio_output_file = cmd.get("audio_output_file", None)
        if audio_output_file:
            cmd["audio_output_file"] = self._get_audio_output_file_for_note(
                audio_output_file, note
            )
        return cmd

    @property
    def commands(self) -> List[Dict[str, Any]]:
        """
        A list of note commands to spawn.
        """
        return [self._get_cmd_for_note(note) for note in self.notes]

    def play(self, **kwargs) -> None:
        """
        Play each `Note` of the Chord in parallel.
        """
        say.spawn(self.commands)

    def cli(self, **kwargs) -> None:
        """
        Handle the execution of this Chord
        within the context of the CLI.
        """
        chord = Chord(**kwargs)
        output_file = kwargs.get("output_file")
        if output_file:
            chord.write(output_file)
        else:
            chord.play(**kwargs)
