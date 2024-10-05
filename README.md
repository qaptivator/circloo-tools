# circloo-tools

# !!! CIRCLIB IS CURRENTLY BROKEN. YOUR LEVEL FILE MAY GET CORRUPTED. !!

Experimental tools for CircloO. Works with CircloO level files. Be sure to backup your levels, **I am not responsible for any data loss or corruption.**

- To use the tools, first install the dependencies (for every tool), like so: `pip install -r requirements.txt`
- Also install `circlib` like so: `git submodule update --init --recursive`
- Run the tools from the top directory, or in other words the repository

## svg_to_level

Parse and insert a SVG file into CircoO level. Does not support quadratic Bezier curves.

Usage: `python -u -m src.svg_to_level`
It will ask for the path to the SVG file (preferably it should be in the same directory as the script).

## circloo_video

Generate and play a video through CircloO level.

Usage: `python -u -m src.circloo_video`
It will ask for the path to the video file (preferably it should be in the same directory as the script), and the resolution for pixel display (in-game).

## beatmap_gen

Generate a beeatmap from a song, and a level (similar to rythm games) from the beatmap.

Usage: `python -u -m src.beatmap_gen`
It will ask for the path to the audio file (preferably it should be in the same directory as the script).

## midi_to_level

Generates music in a level by giving it a midi file. It generates an array of triggers producing sounds, and then the corresponding generators with their delays specified in midi.

Usage: `python -u -m src.midi_to_level`
It will ask for the midi file input (.midi)
