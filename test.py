import pretty_midi

midi = pretty_midi.PrettyMIDI('wiishop.mid')
for instrument in midi.instruments:
    print(instrument.name, instrument.is_drum)