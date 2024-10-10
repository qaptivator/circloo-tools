# circloo-tools

# !!! CIRCLIB IS CURRENTLY BROKEN. MOST TOOLS WILL NOT WORK !!!

Experimental tools for CircloO. Works with CircloO level files. Be sure to backup your levels, **I am not responsible for any data loss or corruption.**

To start using the tools:

1. Install dependencies: `pip install -r requirements.txt`
2. Install circlib: `git submodule update --init --recursive`

Each tool is separated into its own package, and they have their own markdown files documenting the usage.

# Tools

🟩 -- fully tested and ready to use<br>
🟨 -- theoretically works but needs testing and fixes<br>
🟥 -- certainly doesnt work, needs rewriting or in its early stages<br>
🟦 -- concept, idea, development has not even started<br>

| Name          | Description                                                                              | Status |
| ------------- | ---------------------------------------------------------------------------------------- | ------ |
| beatmap_gen   | Generate a beatmap from a song, and a level (similar to rythm games) from the beatmap.   | 🟥     |
| circloo_video | Generate and play a video through a CircloO level.                                       | 🟨     |
| midi_to_level | Play music in a level by converting notes from a MIDI file into generators and triggers. | 🟩     |
| svg_to_level  | Parse and insert a SVG image into CircoO level.                                          | 🟨     |

# TODO

- [ ] fix circlib
- [x] separate tools into their own packages
- [ ] rewrite documentation
- [ ] clean up `utils.py`
- [ ] rewrite all tools to use `argparse`
