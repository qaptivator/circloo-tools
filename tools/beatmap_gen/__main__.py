from circlib.circlib import Level
import numpy as np
import librosa
import math
from ..utils import *

def extract_features(audio_file_path: str):
    y, sr = librosa.load(audio_file_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    print(f'Extracted {len(beat_times)} beat times, {len(onset_times)} onset times, tempo is {tempo.item(0)}.')
    return (tempo, beat_times, onset_times)

# https://stackoverflow.com/questions/8798771/perlin-noise-for-1d
def sin_noise(x):
    return math.ceil(math.sin(2*x) + math.sin(math.pi * x)) + 1

def beatmap_from_features(features: tuple):
    tempo, beat_times, onset_times = features
    res = ''

    # header
    global_offset = 0
    res += f'{global_offset}\n'

    # body
    for time in np.nditer(np.concatenate((beat_times, onset_times))):
        input_type = sin_noise(tempo.item(0) + time) # for further randomization
        beat_offset = time + global_offset
        res += f'{input_type} {beat_offset}\n'

    return res

    # beatmap format
    # first line is header: <global_offset> (global time offset for all beats)
    # rest of it is body: <input_type> <beat_offset> (the input needed for the beat aka the column where it falls, the offset in the audio for the beat)

# properties for each input type
INPUT_TYPE_PROPS = [
    (1375, 1670, 27.33),
    (1455, 1670, 27.33),
    (1535, 1670, 27.33),
    (1620, 1670, 27.33),
]

DISSAPEAR_AFTER = 1
WAIT_BETWEEN_GENERATION = 999999 # 277 hours lol

# tmc <x> <y> <radius> <density> <dissapear after * 60> <wait in between generation * 60> <initial delay * 60>
# we can set the initial delay to be negative, and wait between generation to a large value

def level_from_beatmap(level: Level, beatmap: str):
    lines = beatmap.splitlines()

    # header
    global_offset = int(lines[0])
    lines = lines[1:]
    print(f'Created a beatmap with {len(lines)} beats.')
    objects_added = 0

    # body
    for line in lines:
        input_type, beat_offset = line.split(' ')
        input_type, beat_offset = int(input_type), float(beat_offset)

        if input_type >= len(INPUT_TYPE_PROPS):
            continue

        level.create_object('ball_generator', [
            *INPUT_TYPE_PROPS[input_type],
            1, 
            DISSAPEAR_AFTER * 60, 
            WAIT_BETWEEN_GENERATION * 60,
            -((WAIT_BETWEEN_GENERATION - (beat_offset + global_offset)) * 60),
        ])

        objects_added += 1

    print(f'Added {objects_added} objects to the level.')

def main():
    audio_file_path, level_file_path, save_as_file = get_cli_args([
        { 'prompt': 'Audio file path: ' },
        { 'prompt': 'Level file path (can be empty): ', 'default': 'n' },
        { 'prompt': 'Save as TXT file? (y/n) ', 'default': 'n' }
    ])
    audio_file_path = 'snd_music.ogg'
    level_file_path = 'examples/rythm-game.txt'

    if level_file_path != 'n':
        level = Level.parse(
            ''.join(open(level_file_path, 'r').readlines())
        )
    else:
        level = Level()

    features = extract_features(audio_file_path)

    beatmap = beatmap_from_features(features)
    #open('snd_music.txt', 'w').writelines(beatmap)

    level_from_beatmap(level, beatmap)
    level_text = level.stringify()

    level_output(level_text, save_as_file)

if __name__ == '__main__':
    main()