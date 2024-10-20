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
    return v

TRIGGER_MAPS = {
    'generic': sanitize_trigger_map([
        Instrument(instrument_class='Piano', triggers=[    
            Trigger(midi_number='C2', trigger_variant='piano0'),
            Trigger(midi_number='C#2', trigger_variant='piano1'),
            Trigger(midi_number='D2', trigger_variant='piano2'),
            Trigger(midi_number='D#2', trigger_variant='piano3'),
            Trigger(midi_number='E2', trigger_variant='piano4'),
            Trigger(midi_number='F2', trigger_variant='piano5'),
            Trigger(midi_number='F#2', trigger_variant='piano6'),
            Trigger(midi_number='G2', trigger_variant='piano7'),
            Trigger(midi_number='G#2', trigger_variant='piano8'),
            Trigger(midi_number='A2', trigger_variant='piano9'),
            Trigger(midi_number='A#2', trigger_variant='piano10'),
            Trigger(midi_number='B2', trigger_variant='piano11'),
            Trigger(midi_number='C3', trigger_variant='piano12'),
            Trigger(midi_number='C#3', trigger_variant='piano13'),
            Trigger(midi_number='D3', trigger_variant='piano14'),
            Trigger(midi_number='D#3', trigger_variant='piano15'),
            Trigger(midi_number='E3', trigger_variant='piano16'),
            Trigger(midi_number='F3', trigger_variant='piano17'),
            Trigger(midi_number='F#3', trigger_variant='piano18'),
            Trigger(midi_number='G3', trigger_variant='piano19'),
            Trigger(midi_number='G#3', trigger_variant='piano20'),
            Trigger(midi_number='A3', trigger_variant='piano21'),
            Trigger(midi_number='A#3', trigger_variant='piano22'),
            Trigger(midi_number='B3', trigger_variant='piano23'),
            Trigger(midi_number='C4', trigger_variant='piano24'),
            Trigger(midi_number='C#4', trigger_variant='piano25'),
            Trigger(midi_number='D4', trigger_variant='piano26'),
            Trigger(midi_number='D#4', trigger_variant='piano27'),
            Trigger(midi_number='E4', trigger_variant='piano28'),
            Trigger(midi_number='F4', trigger_variant='piano29'),
            Trigger(midi_number='F#4', trigger_variant='piano30'),
            Trigger(midi_number='G4', trigger_variant='piano31'),
            Trigger(midi_number='G#4', trigger_variant='piano32'),
            Trigger(midi_number='A4', trigger_variant='piano33'),
            Trigger(midi_number='A#4', trigger_variant='piano34'),
            Trigger(midi_number='B4', trigger_variant='piano35'),
            Trigger(midi_number='C5', trigger_variant='piano36'),
            Trigger(midi_number='C#5', trigger_variant='piano37'),
            Trigger(midi_number='D5', trigger_variant='piano38'),
            Trigger(midi_number='D#5', trigger_variant='piano39'),
            Trigger(midi_number='E5', trigger_variant='piano40'),
            Trigger(midi_number='F5', trigger_variant='piano41'),
            Trigger(midi_number='F#5', trigger_variant='piano42'),
            Trigger(midi_number='G5', trigger_variant='piano43'),
            Trigger(midi_number='G#5', trigger_variant='piano44'),
            Trigger(midi_number='A5', trigger_variant='piano45'),
            Trigger(midi_number='A#5', trigger_variant='piano46'),
            Trigger(midi_number='B5', trigger_variant='piano47'),
            Trigger(midi_number='C6', trigger_variant='piano48'),
            Trigger(midi_number='C#6', trigger_variant='piano49'),
            Trigger(midi_number='D6', trigger_variant='piano50'),
            Trigger(midi_number='D#6', trigger_variant='piano51'),
            Trigger(midi_number='E6', trigger_variant='piano52'),
            Trigger(midi_number='F6', trigger_variant='piano53'),
            Trigger(midi_number='F#6', trigger_variant='piano54'),
            Trigger(midi_number='G6', trigger_variant='piano55'),
            Trigger(midi_number='G#6', trigger_variant='piano56'),
            Trigger(midi_number='A6', trigger_variant='piano57'),
            Trigger(midi_number='A#6', trigger_variant='piano58'),
            Trigger(midi_number='B6', trigger_variant='piano59'),
            Trigger(midi_number='C7', trigger_variant='piano60'),
        ])
    ])
}

LAYOUTS = [
    'simple',
    'simple_trimmed',
    'compact_trimmed'
]

class TriggerArray:
    def __init__(self, level, midi, trigger_map: list[Instrument], speed_factor=1, layout=''):
        self.level = level
        self.midi = midi
        self.last_index = 0
        self.end_time = midi.get_end_time()
        self.speed_factor = speed_factor
        self.layout = layout

        # keys are the sounds that can be played (eg C#3), notes are the individual sounds that have their delay
        # array of all supported sounds, basically mapping MIDI notes to real triggers
        self.trigger_map = trigger_map
        # when to wrap the triggers around
        self.triggers_per_row = 10
        # positions of all notes
        self.trigger_position = {}

        # notes extracted from the midi
        self.notes = []

        self.extract_notes()
        self.generate_array()
        self.generate_notes()

    def extract_notes(self):
        for instrument in self.midi.instruments:
            map_instrument = None
            for v in self.trigger_map:
                if (instrument.name in v.instrument_name or pretty_midi.program_to_instrument_class(instrument.program) in v.instrument_class) and instrument.is_drum == v.is_drum:
                    map_instrument = v
                    break
            if not map_instrument:
                continue

            for note in instrument.notes:
                for trigger in map_instrument.triggers:
                    if trigger.midi_number == note.pitch:
                        self.notes.append(Note(trigger, note.start, note.end))
                        break

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
< {self.last_index}'''
            self.last_index += 1
        else:
            print(f'Trigger \'{note.trigger.trigger_variation}\' doesnt have position defined in it, skipping adding sound')

    def get_level(self):
        return self.level
    
    # this is a REALLY janky way of doing this
    def generate_array(self):
        def trim():
            used_triggers = set()
            for note in self.notes:
                used_triggers.add(note.trigger)

            for instrument in self.trigger_map:
                for trigger in instrument.triggers:
                    if trigger not in used_triggers:
                        instrument.triggers.remove(trigger)

        def simple(trigger_padding, trigger_offset):
            for instrument in self.trigger_map:
                                for index, trigger in enumerate(instrument.triggers):
                                    if trigger.trigger_variant:
                                        column = index % self.triggers_per_row
                                        row = math.floor(index / self.triggers_per_row)
                                        pos = (column * trigger_padding[0] + trigger_offset[0], row * trigger_padding[1] + trigger_offset[1])
                                        trigger.trigger_position = pos

                                        self.level += f'''
ic 'im' {pos[0]} {pos[1]} 1  90 0
trigger
sfx \'{trigger.trigger_variant}\' {trigger.trigger_volume} {trigger.trigger_pitch} -1
< {self.last_index}'''
                                        self.last_index += 1

        def compact():
            pass

                                        
        if self.layout not in LAYOUTS:
            return
        match self.layout:
            case 'simple':
                simple((100, 100), (1050, 1050))
            case 'simple_trimmed':
                trim()
                simple((100, 100), (1050, 1050))
            case 'compact_trimmed':
                trim()
                simple((10, 10), (1050, 1050))
        
def main():
    parser = create_argparse(prog='midi_to_level', description='Generates music in a level by converting notes from a MIDI file into generators and triggers. PS \'trimmed\' in a layout means that notes (triggers) not used in the song would not get created, aka they get trimmed.')
    parser.add_argument('midi', action='store', help='Path to MIDI file (.mid)')
    parser.add_argument('-s', '--speed', action='store', type=float, default=1, help='Speed factor which is applied to the MIDI. Defaults to %(default)s.')
    parser.add_argument('-m', '--mapping', action='store', type=str, default='generic', choices=TRIGGER_MAPS.keys(), help='Selects the trigger mapping, which is used to map MIDI notes to level triggers. Defaults to %(default)s.')
    parser.add_argument('-l', '--layout', action='store', type=str, default='simple', choices=LAYOUTS, help='Layout in which triggers will be created and arranged. Defaults to %(default)s.')
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

    trigger_array = TriggerArray(level, midi, trigger_map, args.speed, args.layout)
    level_text = trigger_array.get_level()

    save_level(level_text, args)

if __name__ == '__main__':
    main()