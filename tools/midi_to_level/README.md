# midi_to_level

Play music in a level by converting notes from a MIDI file into generators and triggers. It generates an array of triggers producing sounds, and then the corresponding generators with their delays specified in midi. View the help menu in the CLI.

TODO:

- [x] document cli arguments
- [ ] add customizable layouts (eg straight, square, compact), which will ucstomize the arrangement and padding of triggers
- [ ] remove compact entirely, make it embedded into layouts

Usage: `python -u -m src.midi_to_level`
It will ask for the midi file input (.mid)

Credits to [thisaccountdoesnotexist](https://onlinesequencer.net/members/48437) for example Megalovania no bass midi from [Online Sequencer](https://onlinesequencer.net/1760062)
