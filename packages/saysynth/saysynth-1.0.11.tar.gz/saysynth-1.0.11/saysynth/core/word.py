"""
The Word class contains info on the text, number of syllables,
and list of phonemes in a word. It's used in the `Lyric` class.

<center><img src="/assets/img/nuclear.png"></img></center>
"""
import math
from typing import List


class Word(object):
    def __init__(self, text: str, syllables: int, phonemes: List[str]):
        """
        The Word class contains info on the text, number of syllables,
        and list of phonemes in a word. It's used in the `Lyric` class.
        Args:
            text: The raw text of the word
            syllables: The number of syllables in the word
            phonemes: The list of phonemes in the word
        """
        self.text = text
        self.syllables = syllables
        self.phonemes = phonemes
        self.n_phonemes = len(self.phonemes)
        self.max_phonemes_per_syllable = math.floor(
            self.n_phonemes / self.syllables
        )
