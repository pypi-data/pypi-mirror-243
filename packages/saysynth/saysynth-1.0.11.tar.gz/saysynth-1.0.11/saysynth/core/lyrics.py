"""
The Lyric class enables "singing"-like speech synthesis
by translating input text into a list of phonemes which can
mapped onto musical passages through other `saysynth` functions.
<center><img src="/assets/img/cell.png"></img></center>
"""
from functools import cached_property
from typing import List

from ..lib import nlp
from .word import Word


class Lyrics(object):
    def __init__(self, text: str):
        """
        The Lyric class enables "singing"-like speech synthesis
        by translating input text into a list of phonemes which can
        mapped onto musical passages through other `saysynth` functions.
        Args:
            text: The text of the lyrics. Use punctuation for pauses.
        """
        self.text = text

    def get_phoneme_for_index(self, index: int) -> str:
        """
        Given an index (for instance in an iteration) return
        a phoneme at the respective position. This operation
        uses a modulo such that a text is repeated over and
        over until the full musical passage has been generated.
        """
        seg_index = index % self.n_phonemes
        return self.phonemes[seg_index]

    def get_phonemes(self, start_at: int = 0, end_at: int = -1) -> List[str]:
        """
        Get phonemes of these lyrics between a specific index range.
        """
        return self.phonemes[start_at:end_at]

    @cached_property
    def words(self) -> List[Word]:
        """
        A list of `Word` objects in the text.
        """
        return [Word(*word) for word in nlp.process_text_for_say(self.text)]

    @cached_property
    def n_words(self) -> int:
        """
        The number of syllables in the text.
        """
        return len(self.words)

    @cached_property
    def n_syllables(self) -> int:
        """
        The number of syllables in the text.
        """
        return sum([word.syllables for word in self.words])

    @cached_property
    def phonemes(self) -> List[str]:
        """
        The list of phonemes in the text.
        """
        return [p for word in self.words for p in word.phonemes]

    @cached_property
    def n_phonemes(self) -> int:
        """
        The number of phonemes in the text.
        """
        return len(self.phonemes)
