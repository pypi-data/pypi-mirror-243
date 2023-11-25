<center>
  <a href="/"><img src="https://saysynth.org/assets/img/logo-color.png" width="100%"></img></a>
  <p class="logo-caption">
    <span class="red">Make</span> <span class="orange"> music</span> <span class="yellow"> with </span>
    <span class="green"> Mac's</span> <code><span class="blue">say</span></code></span> <span class="purple">command</span>.
  </p>
</center>
<hr></hr>

<marquee width="100%" direction="right" height="100px">
<code><span class="rainbow-text">saysynth</span></code> only works with Mac OS X versions 12.X and below!!!
</marquee>

# <span class="purple" style='font-size: 16px; font-weight: bold;'>🔊 **Demos** </span>

<code><span class="rainbow-text">saysynth</span></code> sounds like this:

<iframe width="100%" height="300" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1519081741&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe><div style="font-size: 10px; color: #cccccc;line-break: anywhere;word-break: normal;overflow: hidden;white-space: nowrap;text-overflow: ellipsis; font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;font-weight: 100;"><a href="https://soundcloud.com/abelsonlive" title="brian abelson" target="_blank" style="color: #cccccc; text-decoration: none;">brian abelson</a> · <a href="https://soundcloud.com/abelsonlive/sets/saysynth-demos-v100" title="saysynth demos v1.0.0" target="_blank" style="color: #cccccc; text-decoration: none;">saysynth demos v1.0.0</a></div>

You can also purchase recordings of these demos on [bandcamp](https://gltd.bandcamp.com/album/saysynth-demos-v100).

Artwork by [Jeremiah McNair](https://www.instagram.com/jeremiahjmcnair/).

# <span class="purple">🙋 **About** </span>
<hr/>

<code><span class="rainbow-text">saysynth</span></code> is a a synthesizer built on top of Apple's built-in [Speech Synthesis](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/SpeechOverview/SpeechOverview.html#//apple_ref/doc/uid/TP40004365-CH3-SW6) framework, first introduced nearly 30 years ago, [when Steve Jobs demoed "Fred"](https://www.youtube.com/embed/NnsDFSXBWoM). <code><span class="rainbow-text">saysynth</span></code> provides utilities for synthesizing notes, chords, arpeggiated melodies, multi-track sequences and more!

## <span class="blue"> **☞ how it works** </span>

At some point in Fred's development, Apple decided they needed to give developers the ability to control the pitch and speaking rate of his voice. These capabilities were provided via a [domain-specific language](https://en.wikipedia.org/wiki/Domain-specific_language) (DSL) Apple created to allow users to control the duration and pitch contours of individual [phonemes](https://en.wikipedia.org/wiki/Phoneme). Eventually, this DSL was expanded to support "Alex" and "Victoria", two other built-in voices. The syntax for this DSL looks like this:

```
AA {D 120; P 176.9:0 171.4:22 161.7:61}
```

Where `AA` is a [valid phoneme](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/Phonemes/Phonemes.html#//apple_ref/doc/uid/TP40004365-CH9-SW1), `D 120` is the duration of the phoneme in milliseconds, and ` P 176.9:0 171.4:22 161.7:61` represents the pitch contour for the phoneme in colon-separated pairs of frequency and percentage duration.

<code><span class="rainbow-text">saysynth</span></code> works by harnessing this DSL to create musical passages with the `say` command, mapping notes onto their associated frequencies via [`midi-utils`](https://gitlab.com/gltd/midi-utils/), generating phonemes with pitch contours (as described in [Apple's Speech Synthesis Programming Guide](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/SpeechSynthesisProgrammingGuide/FineTuning/FineTuning.html#//apple_ref/doc/uid/TP40004365-CH5-SW7)), and spawning multiple subprocesses in Python to create polyphonic, mostly drone-oriented music. Rudimentary text-to-speech capabilities are provided by [`g2p-en`](https://pypi.org/project/g2p-en/), a library for extracting phonemes from words, though, as of now, some trial and error is necessary to get this sounding intelligible. You can read more about my motivation in building this tool [here](https://brian.abelson.live/log/2023/02/20/making-your-mac-sing.html).

# <span class="purple">🛠️ **Installation** </span>
<hr/>

<code><span class="rainbow-text">saysynth</span></code> only works on Mac OS X machines with a working `say` installation. By default, the path to the executable is set to `/usr/bin/say`. You can override that path by setting the environment variable `SAYSYNTH_SAY_EXECUTABLE`.

## <span class="blue"> **☞ via pypi**  </span>
First, install `python` via [homebrew](https://brew.sh/) (eg: `brew install python`)

Next, run:

```bash
pip install --user --upgrade saysynth
```

You should now be able to run `sy --help`. This command will also update a currently-installed instance of <code><span class="rainbow-text">saysynth</span></code>.

# <span class="purple">💻 **Command-Line Interface (`sy`)** </span>
<hr/>

<code><span class="rainbow-text">saysynth</span></code> is primarily designed to be used via it's command-line interface (`sy` for short).

You can view all commands (and their corresponding docs) by runnings `sy --help`:

```bash
Usage: sy [OPTIONS] COMMAND [ARGS]...

  Make music with the `say` command.

Options:
  --help  Show this message and exit.

Commands:
  chord    Generate a polyphonic chord.
  version  Print the current version of saysynth to the console.
  list     List all currently running saysynth processes.
  midi     Synthesize a melody from a fully-monophonic midi file.
  stop     Stop currently running `say` processes by `sequence`, `track`,...
  font     Given a scale and other parameters, generate a soundfont of...
  arp      Generate an arpeggiated melody.
  demo     Play a built-in demo.
  note     Generate an individual note.
  seq      Play a sequence of `chord`, `midi`, `note`, and/or `arp`...
```

Below are basic details on each command's functionality.

## <span class="blue"> **☞ sy note**  </span>
<hr/>

`sy note` accepts a note name (eg: `C3`) or midi note number (eg: `69`) and generates input to the `say` command which makes a monophonic note.

##### <span class="orange"> examples </span>

Play the note `D#2` randomizing the phoneme each segment by choosing from the `drone`-like phonemes for `Fred`s voice.

```bash
sy note 'D#2' --randomize-phoneme 'Fred:drone' --randomize-segments 'phoneme'
```

You can see the full list of options for this command via `sy note --help`.


## <span class="blue"> **☞ sy arp** </span>
<hr/>

`sy arp` accepts a chord root (eg: `C3`), chord name, and list of styles to generate a melodic, arpeggiated sequence of speech synthesis.

##### <span class="orange"> example </span>

Play an acid-like sequence:

```bash
sy arp 'E0' `# set the root of the arpeggiator to E-1` \
  --chord-notes '0,3,5,7,9,12,14,25,31' `# set the notes of the arpeggiator` \
  --text '. TEE BEE THREE OH THREE  .' `# text to sing` \
  --styles 'down,random_shuffle,random_octaves' `# arpeggiator style names come from the midi-utils module.` \
  --beat-bpm '130' `# the bpm to use when applying the note-count ` \
  --beat-count '1/32' `# the duration of each beat in the arpeggiator` \
  --note-bpm '130' `# the bpm to use when applying the note-count` \
  --note-count '1/32' `# the duration of each note` \
  --segment-bpm '130' `# the bpm to use when applying the segment-count` \
  --segment-count '1/32' `# the duration of each phoneme segment` \
  --velocities '60,90,127' `# a list of velocities to apply in order to the outputted notes` \
  --duration '15000' `# the total duration of the arpeggiator in milliseconds` \
  --render-volume-level-per-note '5' `# see docs` \
  --render-volume-level-per-segment '5' `# see docs`
```

You can see the full list of options for this command via `sy arp --help`.

## <span class="blue"> **☞ sy chord** </span>
<hr/>

`sy chord` accepts a chord root (eg: `C3`) or midi note number (eg: `69`), a chord name (eg: min6), and other parameters to spawn multiple `say` commands that generate a polyphonic chord.

##### <span class="orange"> example </span>

Play a slowly-evolving minor 6th chord:

```bash
sy chord 'C2' `# the root of the chord` \
  --chord 'min6' `# the name of the chord which comes from midi-utils` \
  --duration '45000' `# the duration in ms` \
  --segment-bpm '155' `# the bpm to use when using --segment-count` \
  --segment-count '1/16' `# the duration of each segment in the note` \
  --attack '0.5' --decay '0' --sustain '0.5' --release '0.5' `# ADSR settings` \
  --randomize-segments 'phoneme' `# phoneme-level randomization settings` \
  --voice 'Alex' `# the voice to use, either Fred, Victoria, or Alex` \
  --phoneme 'm,OW,EW' `# list of phonemes to randomly pick from` \
  --volume-range 0.03 0.33 `# min and mix of volume range`
```

You can see the full list of options for this command via `sy chord --help`.


## <span class="blue"> **☞ sy font**  </span>
<hr/>

`sy font` enables the generation of ["soundfonts"](https://www.maniactools.com/soft/midi_converter/soundfonts.shtml) or directories of individual sound files, which can be used in a sampler or DAW to create custom instruments. All synthesis parameters from `sy note` can be modified in `sy font`.

##### <span class="orange"> example </span>

Create a directory of audio files, one per pitch in a specified scale. These can be used to create instruments in a DAW / livecoding environment of your choice:

```bash
mkdir -p tmp `# create an output directory`
sy font \
  --scale-start-at 'C2' `# the lowest note of the scale to generate` \
  --scale-end-at 'C5' `# the highest note of the scale to generate` \
  --key 'C' `# the key of the --scale` \
  --scale 'octatonic_whole' `# the scale to use when selecting the notes to generate. (from midi_utils)` \
  --output-dir 'tmp/' `# the directory to write each file to` \
  --format 'aiff' `# the format of each file` \
  --duration '1000' `# the duration of each file`
```

You can see the full list of options for this command via `sy font --help`.

## <span class="blue"> **☞ sy midi**  </span>
<hr/>

`sy midi` accepts a midi file and generates pitched phonemes. The midi files must be fully monophonic. (In other words there must not be any overlapping notes. Eventually I'll figure out this issue, but for now there is a helpful error message which indicates the name of an overlapping note and the time at which it occurs. You can then use this information to edit your midi file in whatever DAW you use. There is also no support for multi-track midi files, though that will be less challenging to implement.) `sy midi` then maps the notes in the midi file onto pitched phonemes


##### <span class="orange"> example </span>

To run this example, clone this repository and execute the following command from the root directory. Alternatively, generate your own midi file and replace it's path with `examples/arp.mid`.

Play a high-pitched sequence from a a midi file.

```bash
sy midi 'examples/arp.mid' --phoneme 'm'
```

You can see the full list of options for this command via `sy midi --help`.

## <span class="blue"> **☞ sy seq** </span>
<hr/>

`sy seq` accepts a `yaml` filepath specifying multiple <code><span class="rainbow-text">saysynth</span></code> commands to be concurrently executed.

The `yaml` file might look something like this:

```yaml
name: my-sequence          # The name of the sequence. You pass sequence names into `sy stop` or `sy seq stop` to stop all tracks in a sequence at once.
globals:                   # Configurations shared between all tracks
  duration_bpm: 80         # The bpm to use when calculating each tracks duration
  duration_count: 128      # The beat count to use when calculating each tracks duration
tracks:                    # List of tracks / configurations
  chord1:                  # The name of the track. You can use track names to dynamically start/stop each track via the -t flag.
    type: chord            # The type of this track. Either chord, arp, note, or midi.
    options:               # Options to pass to the `chord` function.
                           #   These can also be the shortened versions (eg. 'c' instead of 'chord')
      root: E3             # The root note of the chord
      chord: min6          # The name of the chord
      segment_bpm: 80      # The bpm to use when calculating the length of each segment
      phoneme: 'm,2OW'
  note1:
    type: note
    options:
      phoneme: 'm,2OW'
      start_bpm: 80        # The bpm to use when calculating the start time
      start_count: 4       # Delay the start of this track by a count of 4
      duration_count: 124  # Make the duration of this track shorter than the global setting by a count of 4
      note: F#3            # The note to synthesize.
```

Where `globals` define options shared between all `tracks`, each of which have a `type` which corresponds to a <code><span class="rainbow-text">saysynth</span></code> command (`chord`, `midi`, `note`, and/or `arp`) and a set of `options`.

All commands can also generate a `yaml` version of its parameters by appending the `--yaml` option. For instance `sy note E#3 -rp Fred:note --yaml` would generate something like this:

```yaml
tracks:
- note-b2lw2:
  type: note
  options:
    root: 64
    randomize_phoneme: Fred:note
```
##### <span class="purple"> **subcommands** </span>

`sy seq` provides multiple subcommands to control the behavior of your sequence. These include:

- `play`: Play the sequence as-is, from beginning to end, respecting any `start_*` configurations.
- `start`: Launch all tracks in the sequence immediately, irregardless of any `start_*` configurations.
- `stop`: Stop one or more tracks currently playing from the sequence.
- `echo`: Print the sequence to the console.
- `render`: Render all tracks in the sequence as separate, monophonic audio-files.

Each of these subcommands accepts command line flags, as well. For instance, `--tracks` allows you to
`play`, `start`, `stop`, or `render` only certain tracks in the sequence. Similarly `--audio-devices` allows
you to filter tracks which are configured to play on certain audio outputs.

`--config-overrides` provides the ability to override global and track-level configurations at runtime by passing in yaml-formatted configurations, eg: `-c '{"foo":"bar"}'`. These configurations can be specified at the track-level by nesting them under the track name, eg: `-c '{"track":{"foo":"bar"}}'`.

You can also override configurations by providing extra command line arguments available to `midi`, `note`, `chord`, rand/or `arp` tracks, eg: `-sd 10` or `--segment- duration 10`. These can be similarly nested by using a `__` separator, eg: `--track__segment-duration 10`. Parameters specified via the --config-overrides option will take precedence over any extra CLI arguments.

Finally, `--output-dir` allows you to specify the directory to write audio files into as a part of the `render` command.

##### <span class="orange"> example </span>

To run this example, clone this repository and execute the following command from the root directory. Alternatively, generate your own `yaml` file and replace it's path with `examples/hello-world.yml`.

Launch a multi-track sequence from a `yaml` file and stop it after 10 seconds:

```bash
sy seq play examples/hello-world.yml
sleep 10
sy seq stop examples/hello-world.yml -t hello_world
```

You can also see an archive of my past <code><span class="rainbow-text">saysynth</span></code> [performances](https://gitlab.com/gltd/saysynth/-/tree/main/performances) for examples of sequences.

You can see the full list of options for this command via `sy seq --help`.

## <span class="blue"> **☞ sy stop**  </span>
<hr/>

`sy stop` allows you to stop currently running <code><span class="rainbow-text">saysynth</span></code> processes by `sequences`, `tracks`, `audio_devices`, and/or `parent_pids`.
Omit all the flags to stop all running processes.

##### <span class="orange"> example </span>

Launch a couple notes, wait 10 seconds, and then stop them:

```bash
sy note D#3 -rp Fred:drone
sy note G#3 -rp Fred:drone
sleep 10
echo "stopping all notes now!"
sy stop -t note
```


## <span class="blue"> **☞ sy demo** </span>
<hr/>

`sy demo` is a wrapper for `sy seq` and allows you to play built-in demo sequences. Live recordings of these demos are also for sale on [bandcamp](https://gltd.bandcamp.com/album/saysynth-demos-v100).

##### <span class="orange"> example </span>

Play the built-in demo <code><span class="rainbow-text">fire</span></code>:

```bash
sy demo play fire
```

You can see the full list of built-in demos. for this command via `sy demo --help`.

## <span class="blue"> **☞ sy version** </span>
<hr/>

<code>sy version</code> prints the current version of <code><span class="rainbow-text">saysynth</span></code>

##### <span class="orange"> example </span>

Print the currently-installed version of saysynth:

```
sy version
```

# <span class="purple">🤝🏽 **Development / Contributing** </span>
<hr/>

If you're interested in contributing to <code><span class="rainbow-text">saysynth</span></code> or would like to report [an issue](https://gitlab.com/gltd/saysynth/-/issues), all development is done on [gitlab](https://gitlab.com/gltd/saysynth).  You can also reach out to me via `brian [at] abelson [dot] live`. I'm particularly interested in working with interface designers to turn this into a free VST, or something similar.

To install via `git` for local development:

```bash
git clone https://gitlab.com/gltd/saysynth.git # clone this repo
cd saysynth && python -m venv .venv            # create a virtualenv with Python 3.9 or higher
source .venv/bin/activate                      # activate it
make install                                   # install the library
saysynth --help                                # check if it worked
make test                                      # run the tests
make docs-html && make docs-view               # compile and view the docs (via: pdoc)
```
