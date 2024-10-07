import re

def get_cli_args(inputs):
    res = []
    for input_data in inputs:
        prompt = input_data.get('prompt')
        if prompt:
            default = input_data.get('default')
            input_res = input(prompt)
            if default and not input_res:
                res.append(default)
            elif not default and not input_res:
                raise Exception('This argument is required!')
            elif input_res:
                res.append(input_res)
    return res

def string_to_tuple(str):
    parts = str.split(',')
    return (parts[0].strip(), parts[1].strip())

def list_safe_get(array, index):
    try:
        return array[index]
    except IndexError:
        return None
    except KeyError:
        return None
    
def get_file_name(full_name):
    dot_index = full_name.rfind('.')
    if dot_index != -1: 
        return full_name[:dot_index]
    else:
        return full_name

def num_from_str(v):
    return ''.join(re.findall(r'\d+', v))

def level_output(level_text, save_as_file, file_name='script_output.txt'):
    if save_as_file == 'y':
      print(f'Saving to {file_name}')
      with open(file_name, 'w') as f:
         f.write(level_text)
    else:
      print(level_text)

def find(arr, key, target):
    for x in arr:
        if x[key] == target:
            return x

LEVEL_PREFIX = '''/
/ circloO level
/ Made with circloO Level Editor
totalCircles 7 1
/ EDITOR_TOOL 1 select
/ EDITOR_VIEW 1500 1500 1
/ EDT 111791
/ _SAVE_TIME_1728293280000_END
levelscriptVersion 8
COLORS 246
grav 1 270
'''

PIANO_NOTES = [
    {"midi": "C2", "t_variation": "piano0", "t_pitch": 1, "t_volume": 1},
    {"midi": "C#2", "t_variation": "piano1", "t_pitch": 1, "t_volume": 1},
    {"midi": "D2", "t_variation": "piano2", "t_pitch": 1, "t_volume": 1},
    {"midi": "D#2", "t_variation": "piano3", "t_pitch": 1, "t_volume": 1},
    {"midi": "E2", "t_variation": "piano4", "t_pitch": 1, "t_volume": 1},
    {"midi": "F2", "t_variation": "piano5", "t_pitch": 1, "t_volume": 1},
    {"midi": "F#2", "t_variation": "piano6", "t_pitch": 1, "t_volume": 1},
    {"midi": "G2", "t_variation": "piano7", "t_pitch": 1, "t_volume": 1},
    {"midi": "G#2", "t_variation": "piano8", "t_pitch": 1, "t_volume": 1},
    {"midi": "A2", "t_variation": "piano9", "t_pitch": 1, "t_volume": 1},
    {"midi": "A#2", "t_variation": "piano10", "t_pitch": 1, "t_volume": 1},
    {"midi": "B2", "t_variation": "piano11", "t_pitch": 1, "t_volume": 1},
    {"midi": "C3", "t_variation": "piano12", "t_pitch": 1, "t_volume": 1},
    {"midi": "C#3", "t_variation": "piano13", "t_pitch": 1, "t_volume": 1},
    {"midi": "D3", "t_variation": "piano14", "t_pitch": 1, "t_volume": 1},
    {"midi": "D#3", "t_variation": "piano15", "t_pitch": 1, "t_volume": 1},
    {"midi": "E3", "t_variation": "piano16", "t_pitch": 1, "t_volume": 1},
    {"midi": "F3", "t_variation": "piano17", "t_pitch": 1, "t_volume": 1},
    {"midi": "F#3", "t_variation": "piano18", "t_pitch": 1, "t_volume": 1},
    {"midi": "G3", "t_variation": "piano19", "t_pitch": 1, "t_volume": 1},
    {"midi": "G#3", "t_variation": "piano20", "t_pitch": 1, "t_volume": 1},
    {"midi": "A3", "t_variation": "piano21", "t_pitch": 1, "t_volume": 1},
    {"midi": "A#3", "t_variation": "piano22", "t_pitch": 1, "t_volume": 1},
    {"midi": "B3", "t_variation": "piano23", "t_pitch": 1, "t_volume": 1},
    {"midi": "C4", "t_variation": "piano24", "t_pitch": 1, "t_volume": 1},
    {"midi": "C#4", "t_variation": "piano25", "t_pitch": 1, "t_volume": 1},
    {"midi": "D4", "t_variation": "piano26", "t_pitch": 1, "t_volume": 1},
    {"midi": "D#4", "t_variation": "piano27", "t_pitch": 1, "t_volume": 1},
    {"midi": "E4", "t_variation": "piano28", "t_pitch": 1, "t_volume": 1},
    {"midi": "F4", "t_variation": "piano29", "t_pitch": 1, "t_volume": 1},
    {"midi": "F#4", "t_variation": "piano30", "t_pitch": 1, "t_volume": 1},
    {"midi": "G4", "t_variation": "piano31", "t_pitch": 1, "t_volume": 1},
    {"midi": "G#4", "t_variation": "piano32", "t_pitch": 1, "t_volume": 1},
    {"midi": "A4", "t_variation": "piano33", "t_pitch": 1, "t_volume": 1},
    {"midi": "A#4", "t_variation": "piano34", "t_pitch": 1, "t_volume": 1},
    {"midi": "B4", "t_variation": "piano35", "t_pitch": 1, "t_volume": 1},
    {"midi": "C5", "t_variation": "piano36", "t_pitch": 1, "t_volume": 1},
    {"midi": "C#5", "t_variation": "piano37", "t_pitch": 1, "t_volume": 1},
    {"midi": "D5", "t_variation": "piano38", "t_pitch": 1, "t_volume": 1},
    {"midi": "D#5", "t_variation": "piano39", "t_pitch": 1, "t_volume": 1},
    {"midi": "E5", "t_variation": "piano40", "t_pitch": 1, "t_volume": 1},
    {"midi": "F5", "t_variation": "piano41", "t_pitch": 1, "t_volume": 1},
    {"midi": "F#5", "t_variation": "piano42", "t_pitch": 1, "t_volume": 1},
    {"midi": "G5", "t_variation": "piano43", "t_pitch": 1, "t_volume": 1},
    {"midi": "G#5", "t_variation": "piano44", "t_pitch": 1, "t_volume": 1},
    {"midi": "A5", "t_variation": "piano45", "t_pitch": 1, "t_volume": 1},
    {"midi": "A#5", "t_variation": "piano46", "t_pitch": 1, "t_volume": 1},
    {"midi": "B5", "t_variation": "piano47", "t_pitch": 1, "t_volume": 1},
    {"midi": "C6", "t_variation": "piano48", "t_pitch": 1, "t_volume": 1},
    {"midi": "C#6", "t_variation": "piano49", "t_pitch": 1, "t_volume": 1},
    {"midi": "D6", "t_variation": "piano50", "t_pitch": 1, "t_volume": 1},
    {"midi": "D#6", "t_variation": "piano51", "t_pitch": 1, "t_volume": 1},
    {"midi": "E6", "t_variation": "piano52", "t_pitch": 1, "t_volume": 1},
    {"midi": "F6", "t_variation": "piano53", "t_pitch": 1, "t_volume": 1},
    {"midi": "F#6", "t_variation": "piano54", "t_pitch": 1, "t_volume": 1},
    {"midi": "G6", "t_variation": "piano55", "t_pitch": 1, "t_volume": 1},
    {"midi": "G#6", "t_variation": "piano56", "t_pitch": 1, "t_volume": 1},
    {"midi": "A6", "t_variation": "piano57", "t_pitch": 1, "t_volume": 1},
    {"midi": "A#6", "t_variation": "piano58", "t_pitch": 1, "t_volume": 1},
    {"midi": "B6", "t_variation": "piano59", "t_pitch": 1, "t_volume": 1},
    {"midi": "C7", "t_variation": "piano60", "t_pitch": 1, "t_volume": 1},
]
