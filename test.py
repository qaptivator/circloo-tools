import pretty_midi

midi = pretty_midi.PrettyMIDI('heartache2.mid')
for instrument in midi.instruments:
    print(instrument.name, '-', pretty_midi.program_to_instrument_class(instrument.program))