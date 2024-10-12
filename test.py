import pretty_midi
import re

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

def note_name_to_number(note_name):
    # Map note name to the semitone
    pitch_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    # Relative change in semitone denoted by each accidental
    acc_map = {'#': 1, '': 0, 'b': -1, '!': -1}

    # Reg exp will raise an error when the note name is not valid
    try:
        # Extract pitch, octave, and accidental from the supplied note name
        match = re.match(r'^(?P<n>[A-Ga-g])(?P<off>[#b!]?)(?P<oct>[+-]?\d+)$',
                         note_name)

        pitch = match.group('n').upper()
        offset = acc_map[match.group('off')]
        octave = int(match.group('oct'))
    except:
        raise ValueError('Improper note format: {}'.format(note_name))

    # Convert from the extrated ints to a full note number
    return 12*(octave + 1) + pitch_map[pitch] + offset

result = []


for note in PIANO_NOTES:
    result.append({

    })
note_name_to_number()