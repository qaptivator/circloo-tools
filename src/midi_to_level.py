from .utils import *
import pretty_midi
import math

# TODO: use the inquirer library

class TriggerArray:
    def __init__(self, level_text, midi_data):
        self.level_text = level_text
        self.midi_data = midi_data
        self.last_index = 0
        self.end_time = midi_data.get_end_time()
        self.speed_factor = 1.2

        # array of all supported sounds, basically mapping MIDI notes to real triggers
        self.sounds = PIANO_NOTES
        # when to wrap the triggers around
        self.sounds_per_row = 10
        self.sounds_pos = {}

        self.notes = []

    def generate_array(self):
        padding = (100, 100) # padding between triggers
        offset = (1050, 1050) # offset from the top left corner of the level
    
        for index, sound in enumerate(self.sounds):
            column = index % self.sounds_per_row
            row = math.floor(index / self.sounds_per_row)
            pos = (column * padding[0] + offset[0], row * padding[1] + offset[1])
            self.sounds_pos[sound['t_variation']] = pos

            # regular collectable: ic 'io' {pos[0]} {pos[1]} 1 
            # gravity collectable (nothing on the inside): ic 'im' {pos[0]} {pos[1]} 1  90 0
            self.level_text += f'''ic 'im' {pos[0]} {pos[1]} 1  90 0
trigger
sfx \'{sound['t_variation']}\' {sound['t_volume']} {sound['t_pitch']} -1
< {self.last_index}
'''
            self.last_index += 1

    def extract_notes(self):
        #for instrument in self.midi_data.instruments:
            # TODO: prompt the user to select an instrument
        #    for note in instrument.notes:
        #        pass
        #instrument = self.midi_data.instruments[0]
        for instrument in self.midi_data.instruments:
            for note in instrument.notes:
                note_name = pretty_midi.note_number_to_name(note.pitch).upper()
                if note_name:
                    #piano_note = list_safe_get(self.sounds, note_name)
                    piano_note = find(self.sounds, 'midi', note_name)
                    if piano_note and piano_note['t_variation'] and note.start:
                        self.notes.append({
                            'variation': piano_note['t_variation'],
                            'time': note.start,
                            'pitch': piano_note['t_pitch'] or 1,
                            'volume': piano_note['t_volume'] or 1,
                        })

    def add_sounds_from_midi(self):
        for note in self.notes:
            if note['variation'] and note['time']:
                self.add_sound(note['time'], note['variation'], note['pitch'], note['volume'])

    def add_sound(self, delay, variation, pitch=1, volume=1):
        # Adds a generator (note) with specified delay and sound (paino key)
        # wait in between gen will be set to the midi's length, and the initial delay will be negative
        # tmc <x> <y> <radius> <density> <dissapear after * 60> <wait in between gen * 60> <initial delay * 60>

        delay /= self.speed_factor

        radius = 15
        dissapear_after = 0.05

        pos = self.sounds_pos[variation]
        if pos:
            self.level_text += f'''
tmc {pos[0]} {pos[1]} {radius} 0 {dissapear_after * 60} {self.end_time * 60} {-(self.end_time - delay) * 60}
< {self.last_index}
'''
            self.last_index += 1
        else:
            print(f'position for variation \'{variation}\' does not exist, skipping adding sound')

    def get_level(self):
        return self.level_text
        
def main():
    midi_file_path, save_as_file = get_cli_args([
        { 'prompt': 'MIDI file path: ' },
        { 'prompt': 'Save as TXT file? (y/n) ', 'default': 'n' }
    ])

    level_text = ''
    level_text += LEVEL_PREFIX

    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    if not midi_data:
        print("Could not read MIDI file")
        return

    # this is a really bad way of doing this but ok
    trigger_array = TriggerArray(level_text, midi_data)
    trigger_array.generate_array()
    trigger_array.extract_notes()
    trigger_array.add_sounds_from_midi()
    level_text = trigger_array.get_level()

    level_output(level_text, save_as_file)

if __name__ == '__main__':
    main()