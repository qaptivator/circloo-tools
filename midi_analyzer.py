# midi_analyzer.py
# shows general info about the midi song
# useful when converting midis using midi to level
# i hate this script honestly, one of the worst script i have ever written
# see https://www.ccarh.org/courses/253/handout/gminstruments/ for general midi specification

import pretty_midi
from sys import argv
from os import path
from collections import Counter

def to_zero(v):
    return v if v >= 0 else 0

#def get_instrument_name(v):
#    return f'{v.name} ({v.program})'

def get_instrument_name(v):
    return v.name

if __name__ == '__main__':
    if len(argv) > 1:
        if path.exists(argv[1]):
            midi = pretty_midi.PrettyMIDI(argv[1])

            print('\nGeneral:')
            print(f'  File name: {path.basename(argv[1])}')
            print(f'  End time: {round(midi.get_end_time(), 2)}s')
            print(f'  Estimated tempo: {round(midi.estimate_tempo(), 2)}bpm')

            instrument_classes = []
            #ic_max_length = len(max(midi.instruments, key=lambda x: len((x.name))))
            ic_max_length = 0
            for instrument in midi.instruments:
                if len(get_instrument_name(instrument)) > ic_max_length:
                    ic_max_length = len(get_instrument_name(instrument))

            icd_max_length = 0
            for instrument in midi.instruments:
                instrument_class = pretty_midi.program_to_instrument_class(instrument.program)
                if len(instrument_class) > icd_max_length:
                    icd_max_length = len(instrument_class)

            print('\nInstruments:')
            for instrument in midi.instruments:
                instrument_class = pretty_midi.program_to_instrument_class(instrument.program)
                instrument_classes.append(instrument_class)
                print(f'  {get_instrument_name(instrument)}{" " * to_zero(ic_max_length - len(get_instrument_name(instrument)))} // {instrument_class}{" " * to_zero(icd_max_length - len(instrument_class))} // {"drum" if instrument.is_drum else "not drum"}')

            instrument_classes = Counter(instrument_classes)
            total_instrument_classes = len(instrument_classes)
            print('\nInstrument classes:')
            for element, count in instrument_classes.items():
                percentage = round((count / total_instrument_classes) * 100)
                print(f'  {element} ({percentage}%)')
        else:
            print('file by path not found')
    else:
        print('path argument is missing')