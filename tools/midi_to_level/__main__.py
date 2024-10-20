from tools.utils import *
import pretty_midi
import math
import os
from dataclasses import dataclass

# GENERAL MIDI: https://www.ccarh.org/courses/253/handout/gminstruments/
# how to run: python -m tools.midi_to_level --help

@dataclass
class Trigger:
    midi_number: str # the midi note number, aka the pitch. it can be a number, piano key or drum
    trigger_variant: str # the variant used in the trigger (it should be like it's saed in the level file, not like in game)
    trigger_pitch: int = 1 # the pitch in the trigger
    trigger_volume: int = 1 # the volume in the trigger
    trigger_position: tuple[float, float] = (0, 0) # the position of the trigger in editor. should not be defined during creation, this is defined during layout execution.

@dataclass
class Instrument:
    triggers: list[Trigger] # list of actual trigger mappings
    instrument_name: str | list[str] = '' # matches the exact instrument name, or an array of names. see INSTRUMENT_MAP in pretty_midi
    instrument_class: str | list[str] = '' # matches the exact instrument class, or an array of classes. see INSTRUMENT_CLASSES in pretty_midi
    is_drum: bool = False # is this instrument a drum?

@dataclass
class Note:
    trigger: Trigger # the trigger this note uses
    start: float # start time of the note
    end: float # end time of the note (not used)

def sanitize_trigger_map(v: list[Instrument]):
    for instr in v:
        if type(instr.instrument_name) != list:
            instr.instrument_name = [instr.instrument_name]
        if type(instr.instrument_class) != list:
            instr.instrument_class = [instr.instrument_class]
        for trigger in instr.triggers:
            stop_exec = False
            midi_number = trigger.midi_number

            try:
                midi_number = int(midi_number)
            except:
                pass
            else:
                stop_exec = True

            if not stop_exec:
                try:
                    midi_number = pretty_midi.note_name_to_number(midi_number)
                except:
                    pass
                else:
                    stop_exec = True

            if not stop_exec:
                try:
                    midi_number = pretty_midi.drum_name_to_note_number(midi_number)
                except:
                    pass
                else:
                    stop_exec = True

            trigger.midi_number = midi_number

TRIGGER_MAPS = {
    'generic': sanitize_trigger_map([
        Instrument(instrument_class='Piano', triggers=[
            Trigger(midi_number='C2', trigger_variant='piano0'),
        ])
    ])
}

LAYOUTS = [
    'simple'
]

# this is a REALLY janky way of doing this
# function which turns array of triggers into level positions
# trigger_map: list[Instrument] - the trigger map used in generation
# returns: list[Instrument] - the modified trigger map with trigger_position defined. it is not checked anywhere so if something is wrong, you wont know.
def execute_layout(name, trigger_map, array):
    if name not in LAYOUTS:
        return
    match name:
        case 'simple':
            if array.compact:
                new_trigger_map = []
                for key in array.trigger_map:
                    if list_find(array.notes, 'variation', key['t_variation']):
                        new_trigger_map.append(key)
                        
            for index, key in enumerate(new_trigger_map):
                # if a note doesnt exist and it is compact mode, dont generate it. this code isnt needed but ok, i will remove it later
                if list_find(array.notes, 'variation', key['t_variation']) or not array.compact:
                    column = index % array.triggers_per_row
                    row = math.floor(index / self.triggers_per_row)
                    pos = (column * array.trigger_padding[0] + array.trigger_offset[0], row * array.trigger_padding[1] + array.trigger_offset[1])
                    array.trigger_position[key['t_variation']] = pos

                    # regular collectable: ic 'io' {pos[0]} {pos[1]} 1 
                    # gravity collectable (nothing on the inside): ic 'im' {pos[0]} {pos[1]} 1  90 0
                    array.level += f'''
    ic 'im' {pos[0]} {pos[1]} 1  90 0
    trigger
    sfx \'{key['t_variation']}\' {key['t_volume']} {key['t_pitch']} -1
    < {array.last_index}
        '''
                    array.last_index += 1


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
    def __init__(self, level, midi, trigger_map: list[Instrument], compact=False, speed_factor=1, layout=''):
        self.level = level
        self.midi = midi
        self.last_index = 0
        self.end_time = midi.get_end_time()
        self.compact = compact
        self.speed_factor = speed_factor
        self.layout = layout

        # keys are the sounds that can be played (eg C#3), notes are the individual sounds that have their delay
        # array of all supported sounds, basically mapping MIDI notes to real triggers
        self.trigger_map = trigger_map
        # when to wrap the triggers around
        self.triggers_per_row = 10
        # positions of all notes
        self.trigger_position = {}

        # padding between triggers
        self.trigger_padding = (100, 100)
        # offset from the top left corner of the level
        self.trigger_offset = (1050, 1050)

        # notes extracted from the midi
        self.notes = []

        self.extract_notes()
        self.generate_array()
        self.generate_notes()

    def extract_notes(self):
        for instrument in self.midi.instruments:
            map_instrument = None
            for v in self.trigger_map:
                if (instrument.name in v.instrument_name or pretty_midi.program_to_instrument_class(instrument.program) in v.instrument_name) and instrument.is_drum in v.is_drum:
                    map_instrument = v
                    break
            if not map_instrument:
                continue

            for note in instrument.notes:
                trigger = list_find(map_instrument.triggers, 'midi_number', note.pitch)
                if trigger:
                    self.notes.append(Note(trigger, note.start, note.end))
                else:
                    print('skipped trigger')

    def generate_array(self):
        self.trigger_map = execute_layout(self.layout, self.trigger_map, self)

    def generate_notes(self):
        for note in self.notes:
            if note.start and note.trigger:
                self.add_sound(note)

    def add_sound(self, note: Note):
        # Adds a generator (note) based on the note object
        # wait in between gen will be set to the midi's length, and the initial delay will be negative
        # tmc <x> <y> <radius> <density> <dissapear after * 60> <wait in between gen * 60> <initial delay * 60>

        delay = note.start / self.speed_factor
        radius = 15
        dissapear_after = 0.05

        pos = note.trigger.trigger_position
        if pos:
            self.level += f'''
tmc {pos[0]} {pos[1]} {radius} 0 {dissapear_after * 60} {self.end_time * 60} {-(self.end_time - delay) * 60}
noanim
< {self.last_index}
'''
            self.last_index += 1
        else:
            print(f'Trigger \'{note.trigger.trigger_variation}\' doesnt have position defined in it, skipping adding sound')

    def get_level(self):
        return self.level
        
def main():
    parser = create_argparse(prog='midi_to_level', description='Generates music in a level by converting notes from a MIDI file into generators and triggers.')
    parser.add_argument('midi', action='store', help='Path to MIDI file (.mid)')
    parser.add_argument('-c', '--compact', action='store_true', help='Removes triggers for notes, which arent used in the MIDI. By default, the tool creates an array of triggers for all of the available notes.')
    parser.add_argument('-s', '--speed', action='store', type=float, default=1, help='Speed factor which is applied to the MIDI. Defaults to %(default)s.')
    parser.add_argument('-m', '--mapping', action='store', type=str, default='generic', choices=[TRIGGER_MAPS.keys()], help='Selects the trigger mapping, which is used to map MIDI notes to level triggers. Defaults to %(default)s.')
    parser.add_argument('-l', '--layout', action='store', type=str, default='straight', choices=['straight', 'box', 'compact'], help='Layout in which triggers will be created. In a straight line, in a box, compact etc. WORK IN PROGRESS.')
    args = parser.parse_args()

    level = ''
    level += LEVEL_PREFIX

    if not os.path.exists(args.midi):
        print('MIDI file does not exist by the provided path')
        return
    
    midi = pretty_midi.PrettyMIDI(args.midi)
    if not midi:
        print('Could not read MIDI file, an error occured')
        return
    
    trigger_map = TRIGGER_MAPS.get(args.mapping)
    if not trigger_map:
        print(f'Trigger mapping \'{args.mapping}\' doesnt exist')
        return

    trigger_array = TriggerArray(level, midi, trigger_map, args.compact, args.speed, args.layout)
    level_text = trigger_array.get_level()

    save_level(level_text, args)

if __name__ == '__main__':
    main()