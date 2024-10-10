from ..utils import *
import pretty_midi
import math
import os

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
        self.key_map = PIANO_NOTES
        # when to wrap the triggers around
        self.keys_per_row = 10
        # positions of all notes
        self.key_pos = {}

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
        compacted_key_map = self.key_map

        if self.compact:
            compacted_key_map = []
            for key in self.key_map:
                if find(self.notes, 'variation', key['t_variation']):
                    compacted_key_map.append(key)
                    
        for index, key in enumerate(compacted_key_map):
            # if a note doesnt exist and it is compact mode, dont generate it. this code isnt needed but ok, i will remove it later
            if find(self.notes, 'variation', key['t_variation']) or not self.compact:
                column = index % self.keys_per_row
                row = math.floor(index / self.keys_per_row)
                pos = (column * self.trigger_padding[0] + self.trigger_offset[0], row * self.trigger_padding[1] + self.trigger_offset[1])
                self.key_pos[key['t_variation']] = pos

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
                    piano_note = find(self.key_map, 'midi_key', note_name)
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

        pos = list_safe_get(self.key_pos, variation)
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