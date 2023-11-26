#!/usr/bin/env python
"""
This script aids in categorizing phonemes as drone-y, noise-y, or note-y for each voice
"""
from collections import defaultdict
from pprint import pprint

import click

from saysynth.constants import SAY_ALL_PHONEMES, SAY_TUNED_VOICES
from saysynth.lib import say

TEXT_PATTERN = (
    "[[inpt TUNE]] ~"
    " %s {D 800; P 65.41:0 65.41:100}"
    " %s {D 800; P 65.41:0 65.41:100}"
    " %s {D 800; P 65.41:0 65.41:100}"
    " ~ [[inpt TEXT]]"
)

CLASSIFICATIONS = {"d": "drone", "s": "noise", "e": "note", "r": "discard"}


@click.command()
def main():
    classifications = defaultdict(lambda: defaultdict(list))
    for voice in SAY_TUNED_VOICES:
        for phoneme in SAY_ALL_PHONEMES:
            text = TEXT_PATTERN % (phoneme, phoneme, phoneme)
            while 1:
                say.run(input_text=text, voice=voice, parent_pid=None)
                question = f'Does this phoneme "{phoneme}" for {voice} sound like a drone(d), noise(s), note(e), or discard(r)? Or should I repeat(t) it?'
                answer = click.prompt(
                    question, type=click.Choice(["d", "s", "e", "r", "t"])
                )
                if answer != "t":
                    # repeat the command
                    break
            classification = CLASSIFICATIONS.get(answer)
            if classification == "discard":
                click.echo(f"Okay, I'll discard {phoneme} for {voice}")
            click.echo(
                f'Got it! Recording "{phoneme}" as a {classification} for {voice}'
            )
            classifications[voice][classification].append(phoneme)
    click.echo("Done! Here are you classifications:\n")
    pprint(dict(**classifications))


if __name__ == "__main__":
    main()
