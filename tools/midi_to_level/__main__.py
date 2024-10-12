from ..utils import *
import pretty_midi
import math
import os
from dataclasses import dataclass

INSTRUMENT_CLASSES = [

]

@dataclass
class Trigger:
    instrument_class: str
    note_pitch: int

'''
trigger

instrument_class: instrument class which this trigger corresponds to
note_pitch: the note's pitch (piano key, drum thing etc)
->
trigger_variant: variant of the created trigger (the type of instrument is stored inside the variant)
trigger_pitch: pitch of the created trigger
trigger_volume: volume of the created trigger'''

PIANO_NOTES = [
    {"midi_key": "C2", "t_variation": "piano0", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C#2", "t_variation": "piano1", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D2", "t_variation": "piano2", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D#2", "t_variation": "piano3", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "E2", "t_variation": "piano4", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F2", "t_variation": "piano5", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F#2", "t_variation": "piano6", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G2", "t_variation": "piano7", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G#2", "t_variation": "piano8", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A2", "t_variation": "piano9", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A#2", "t_variation": "piano10", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "B2", "t_variation": "piano11", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C3", "t_variation": "piano12", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C#3", "t_variation": "piano13", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D3", "t_variation": "piano14", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D#3", "t_variation": "piano15", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "E3", "t_variation": "piano16", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F3", "t_variation": "piano17", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F#3", "t_variation": "piano18", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G3", "t_variation": "piano19", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G#3", "t_variation": "piano20", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A3", "t_variation": "piano21", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A#3", "t_variation": "piano22", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "B3", "t_variation": "piano23", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C4", "t_variation": "piano24", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C#4", "t_variation": "piano25", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D4", "t_variation": "piano26", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D#4", "t_variation": "piano27", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "E4", "t_variation": "piano28", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F4", "t_variation": "piano29", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F#4", "t_variation": "piano30", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G4", "t_variation": "piano31", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G#4", "t_variation": "piano32", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A4", "t_variation": "piano33", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A#4", "t_variation": "piano34", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "B4", "t_variation": "piano35", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C5", "t_variation": "piano36", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C#5", "t_variation": "piano37", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D5", "t_variation": "piano38", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D#5", "t_variation": "piano39", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "E5", "t_variation": "piano40", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F5", "t_variation": "piano41", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F#5", "t_variation": "piano42", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G5", "t_variation": "piano43", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G#5", "t_variation": "piano44", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A5", "t_variation": "piano45", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A#5", "t_variation": "piano46", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "B5", "t_variation": "piano47", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C6", "t_variation": "piano48", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C#6", "t_variation": "piano49", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D6", "t_variation": "piano50", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "D#6", "t_variation": "piano51", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "E6", "t_variation": "piano52", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F6", "t_variation": "piano53", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "F#6", "t_variation": "piano54", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G6", "t_variation": "piano55", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "G#6", "t_variation": "piano56", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A6", "t_variation": "piano57", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "A#6", "t_variation": "piano58", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "B6", "t_variation": "piano59", "t_pitch": 1, "t_volume": 1},
    {"midi_key": "C7", "t_variation": "piano60", "t_pitch": 1, "t_volume": 1},
]


class TriggerArray:
    def __init__(self, level, midi, compact=False, speed_factor=1):
        self.level = level
        self.midi = midi
        self.last_index = 0
        self.end_time = midi.get_end_time()
        self.compact = compact
        self.speed_factor = speed_factor

        # keys are the sounds that can be played (eg C#3), notes are the individual sounds that have their delay
        # array of all supported sounds, basically mapping MIDI notes to real triggers
        self.trigger_map = PIANO_NOTES
        # when to wrap the triggers around
        self.triggers_per_row = 10
        # positions of all notes
        self.trigger_pos = {}

        # padding between triggers
        self.trigger_padding = (100, 100)
        # offset from the top left corner of the level
        self.trigger_offset = (1050, 1050)

        # notes extracted from the midi
        self.notes = []

        self.extract_notes()
        self.generate_array()

        for note in self.notes:
            if note['time'] and note['variation']:
                self.add_sound(note['time'], note['variation'])

    def generate_array(self):
        new_trigger_map = self.trigger_map

        if self.compact:
            new_trigger_map = []
            for key in self.trigger_map:
                if list_find(self.notes, 'variation', key['t_variation']):
                    new_trigger_map.append(key)
                    
        for index, key in enumerate(new_trigger_map):
            # if a note doesnt exist and it is compact mode, dont generate it. this code isnt needed but ok, i will remove it later
            if list_find(self.notes, 'variation', key['t_variation']) or not self.compact:
                column = index % self.triggers_per_row
                row = math.floor(index / self.triggers_per_row)
                pos = (column * self.trigger_padding[0] + self.trigger_offset[0], row * self.trigger_padding[1] + self.trigger_offset[1])
                self.trigger_pos[key['t_variation']] = pos

                # regular collectable: ic 'io' {pos[0]} {pos[1]} 1 
                # gravity collectable (nothing on the inside): ic 'im' {pos[0]} {pos[1]} 1  90 0
                self.level += f'''
ic 'im' {pos[0]} {pos[1]} 1  90 0
trigger
sfx \'{key['t_variation']}\' {key['t_volume']} {key['t_pitch']} -1
< {self.last_index}
    '''
                self.last_index += 1

    def extract_notes(self):
        #for instrument in self.midi_data.instruments:
            # TODO: prompt the user to select an instrument
        #    for note in instrument.notes:
        #        pass
        #instrument = self.midi_data.instruments[0]
        for instrument in self.midi.instruments:
            for note in instrument.notes:
                note_name = pretty_midi.note_number_to_name(note.pitch).upper()
                if note_name:
                    #piano_note = list_safe_get(self.sounds, note_name)
                    piano_note = list_find(self.trigger_map, 'midi_key', note_name)
                    if piano_note and piano_note['t_variation'] and note.start:
                        self.notes.append({
                            'variation': piano_note['t_variation'],
                            'time': note.start,
                        })

    def add_sound(self, delay, variation):
        # Adds a generator (note) with specified delay and sound (paino key)
        # wait in between gen will be set to the midi's length, and the initial delay will be negative
        # tmc <x> <y> <radius> <density> <dissapear after * 60> <wait in between gen * 60> <initial delay * 60>

        delay /= self.speed_factor

        radius = 15
        dissapear_after = 0.05

        pos = list_safe_get(self.trigger_pos, variation)
        if pos:
            self.level += f'''
tmc {pos[0]} {pos[1]} {radius} 0 {dissapear_after * 60} {self.end_time * 60} {-(self.end_time - delay) * 60}
noanim
< {self.last_index}
'''
            self.last_index += 1
        else:
            print(f'Key for variation \'{variation}\' does not exist, skipping adding sound')

    def get_level(self):
        return self.level
        
def main():
    parser = create_argparse(prog='midi_to_level', description='Generates music in a level by converting notes from a MIDI file into generators and triggers.')
    parser.add_argument('midi', action='store', help='Path to MIDI file (.mid)')
    parser.add_argument('-c', '--compact', action='store_true', help='Removes triggers for notes, which arent used in the MIDI. By default, the tool creates an array of triggers for all of the available notes.')
    parser.add_argument('-s', '--speed', action='store', type=float, default=1, help='Speed factor which is applied to the MIDI.')
    args = parser.parse_args()

    level = ''
    level += LEVEL_PREFIX

    if not os.path.exists(args.midi):
        print("MIDI file does not exist by the provided path")
        return
    
    midi = pretty_midi.PrettyMIDI(args.midi)
    if not midi:
        print("Could not read MIDI file, an error occured")
        return

    trigger_array = TriggerArray(level, midi, args.compact, args.speed)
    level_text = trigger_array.get_level()

    save_level(level_text, args)

if __name__ == '__main__':
    main()