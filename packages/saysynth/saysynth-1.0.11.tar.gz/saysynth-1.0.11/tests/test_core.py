from saysynth.core import Arp, Chord, Lyrics, MidiTrack, Note, Segment, Word
from saysynth.utils import here


def test_segment():
    segment = Segment(note="A3", velocity=127, duration=100)
    assert segment.to_text() == "[[ volm 1.0 ]] 2m {D 100; P 440:0}"


def test_note():
    note = Note(
        note="C4",
        phoneme="m",
        velocity=127,
        attack=0.1,
        decay=0.2,
        sustain=0.3,
        release=0.5,
        bpm=126,
        count=1 / 2,
        segment_bpm=126,
        volume_range=[0.1, 0.5],
        segment_count=1 / 32,
    )
    assert (
        note.segments[0].to_text()
        == "[[ volm 0.1 ]] m {D 59.5238; P 523.25:0}"
    )
    assert (
        note.segments[-1].to_text()
        == "[[ volm 0.108 ]] m {D 35.7143; P 523.25:0}"
    )


def test_lyrics():
    lyrics = Lyrics("hello world")
    assert len(lyrics.words) == 2
    assert [isinstance(word, Word) for word in lyrics.words]


def test_midi_file():
    mf = MidiTrack(midi_file=(here(__file__, "fixtures/valid.mid")))
    assert len(mf.notes) == 27
    assert mf.notes[0].name == "C2"


def test_arp():

    arp = Arp(
        text="hello world", notes=[50, 55, 57, 69], loops=2, styles=["down"]
    )
    assert arp.notes[0].note == 69
    assert arp.n_notes == 16  # (1 for note on 1 for silence)


def test_chord():

    chord = Chord(root="A3", chord_notes=[0, 3, 5, 6])
    assert chord.n_notes == 4
    assert chord.notes[0].name == "A3"
    assert chord.notes[-1].name == "EB4"
