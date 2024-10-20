# midi_to_level

Play music in a level by converting notes from a MIDI file into generators and triggers. It generates an array of triggers producing sounds, and then the corresponding generators with their delays specified in midi. View the help menu in the CLI.

TODO:

- [x] document cli arguments
- [x] add customizable layouts (eg straight, square, compact), which will ucstomize the arrangement and padding of triggers
- [x] remove compact entirely, make it embedded into layouts
- [ ] fix "trimmed" layouts not working correctly (they dont trim at all)

Usage: `python -u -m src.midi_to_level`
It will ask for the midi file input (.mid)

Credits to these people from [Online Sequencer](https://onlinesequencer.net/1760062) for the great midi songs i used while testing and showing off the tool: [thisaccountdoesnotexist](https://onlinesequencer.net/members/48437), [UT Composer](https://onlinesequencer.net/members/14333), [FlyingBacon](https://onlinesequencer.net/members/17926)
