from .utils import *
import pretty_midi

# TODO: use the inquirer library

class TriggerArray:
    def __init__(self, level_text, midi_data):
        self.level_text = level_text
        self.midi_data = midi_data

        # array of all supported sounds, basically mapping MIDI notes to real triggers
        self.sounds = [
            {
                'midi': '5c',
                't_variation': 'piano20',
                't_pitch': 1,
                't_volume': 1,
            }
        ]
        # when to wrap the triggers around
        self.sounds_per_row = 10

        self.notes = []

    def extract_notes(self):
        for instrument in self.midi_data.instruments:
            # TODO: prompt the user to select an instrument
            for note in instrument.notes:
                pass


    def generate_array(self):
        pass

    def add_sounds_from_midi(self):
        pass

    def add_sound(self, delay, note):
        # Adds a generator (note) with specified delay and sound (paino key)
        pass

    def get_level(self):
        return self.level_text
        
def main():
    midi_file_path, level_file_path, save_as_file = get_cli_args([
        { 'prompt': 'MIDI file path: ' },
        { 'prompt': 'Level file path (can be empty): ', 'default': 'n' },
        { 'prompt': 'Save as TXT file? (y/n) ', 'default': 'n' }
    ])

    if level_file_path != 'n':
        level_text = ''.join(open(level_file_path, 'r').readlines())
    else:
        level_text = ''

    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    if not midi_data:
        print("Could not read MIDI file")
        return

    trigger_array = TriggerArray(level_text, midi_data)
    trigger_array.generate_array()
    trigger_array.add_sounds_from_midi()
    level_text = trigger_array.get_level()

    level_output(level_text, save_as_file)

if __name__ == '__main__':
    main()