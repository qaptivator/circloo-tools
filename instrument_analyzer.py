# instrument_analyzer.py
# shows info about every instrument in the midi song
# useful when converting midis using midi to level

import pretty_midi
from sys import argv
from os import path

if __name__ == '__main__':
    if len(argv) > 1:
        if path.exists(argv[1]):
            midi = pretty_midi.PrettyMIDI(argv[1])
            for instrument in midi.instruments:
                print(instrument.name, '-', pretty_midi.program_to_instrument_class(instrument.program), '-', 'drum' if instrument.is_drum else 'not drum')
        else:
            print('file by path not found')
    else:
        print('path argument is missing')