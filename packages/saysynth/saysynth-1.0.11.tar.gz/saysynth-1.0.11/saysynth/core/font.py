"""
The Font class creates a list of `Notes` within a scale and writes them to separate files. This makes them easy to import into samplers or DAWs.
<center><img src="/assets/img/sun-wavy.png"></img></center>
"""
import os
from typing import Union

from midi_utils import midi_scale, midi_to_note, note_to_midi

from .note import Note


class Font(object):
    def __init__(
        self,
        key: Union[str, int],
        scale: str,
        scale_start_at: Union[int, str],
        scale_end_at: Union[int, str],
        **note_options,
    ):
        """
        The Font class creates a list of `Notes` within a
        scale and writes them to separate files. This
        makes them easy to import into samplers or DAWs.
        Scale generation is provided by `midi_scale`
        Args:
            key: The root note of the scale, eg: C,D,G#,etc
            scale: The name of the scale (see midi_utils.constants.SCALES)
            scale_start_at: A note name or midi note number to start the scale at
            scale_end_at: A note name or midi note number to end the scale at
            **note_options: Additional options to pass to `Note` generation.
        """
        # add note type to simplify function call
        self.scale = midi_scale(
            key=key,
            scale=scale,
            min_note=note_to_midi(scale_start_at),
            max_note=note_to_midi(scale_end_at),
        )
        note_options.setdefault("type", "note")
        self.note_options = note_options

    def _get_kwargs(self, midi, kwargs) -> dict:
        kw = dict(self.note_options)
        kw.update(kwargs)
        kw["type"] = "note"
        kw["midi"] = midi
        kw["note"] = midi_to_note(midi)
        return kw

    def play(self, **kwargs) -> None:
        """
        Alias of `self.generate`
        """
        return self.generate(**kwargs)

    def generate(self, **kwargs) -> None:
        # generate files for each note in the scale
        if not os.path.exists(kwargs["output_dir"]):
            os.makedirs(kwargs["output_dir"], exist_ok=True)
        for midi in self.scale:
            kwargs = self._get_kwargs(midi, kwargs)

            # generate audio output file name
            filepath = (
                f"{midi:03d}_{kwargs['note']}_"
                f"{kwargs['voice'].lower()}_{kwargs['rate']}.{kwargs['format']}"
            )
            audio_output_file = os.path.join(
                kwargs["output_dir"],
                filepath,
            )
            # generate input file of text
            note = Note(**kwargs)
            note.play(
                voice=kwargs["voice"],
                rate=kwargs["rate"],
                audio_output_file=audio_output_file,
                wait=True,
            )
            if not os.path.exists(audio_output_file):
                raise RuntimeError(
                    f"File {audio_output_file} was not successfully created"
                )
