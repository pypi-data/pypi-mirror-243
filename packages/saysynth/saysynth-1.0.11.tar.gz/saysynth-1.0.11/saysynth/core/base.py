"""
The `SayObject` class provides standard runtime functionality to monotonic features like `arp`, `note`, and `midi_track`.
<center><img src="/assets/img/nuclear.png"></img></center>
"""
import sys

from ..cli.options import prepare_options_for_say
from ..constants import SAY_TUNE_TAG
from ..lib import say


class SayObject(object):
    def to_text(self):
        """Render this object as Apple SpeechSynthesis DSL text"""
        raise NotImplementedError

    def to_say_text(self):
        """
        Render this object as Apple SpeechSynthesis DSL text,
        including the initial [[TUNE]] tag.
        """
        return SAY_TUNE_TAG + "\n" + self.to_text()

    def write(self, output_file) -> None:
        """
        Render this Arp as Apple SpeechSynthesis DSL text,
        and write it to an output file
        """
        with open(output_file, "w") as f:
            f.write(self.to_say_text())

    def play(self, **say_options) -> None:
        """
        Play this object and pass in additional options to `say.run`
        """
        text = self.to_say_text()
        options = prepare_options_for_say(text, **say_options)
        say.run(**options)

    @classmethod
    def new(cls, **kwargs):
        """
        Instantiate this object.
        """
        return cls(**kwargs)

    def cli(self, **kwargs) -> None:
        """
        Handle the execution of this object
        within the context of the CLI.
        """
        klass = self.new(**kwargs)
        output_file = kwargs.get("output_file")
        if output_file:
            klass.write(output_file)
        elif kwargs.get("no_exec", False):
            sys.stdout.write(klass.to_say_text())
        else:
            klass.play(**kwargs)
