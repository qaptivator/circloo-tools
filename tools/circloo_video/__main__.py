from circlib.circlib import Level
import cv2
import numpy as np
from PIL import Image
from ..utils import *

class Display:
    def __init__(self, level, shape):
        self.level = level
        self.shape = shape

        self.pixel_size = 30
        self.pixel_origin = inv_center_point((1500, 1000), self.real_shape()) # origin of the pixel display
        self.pixels = np.empty(self.shape)
        self.pixel_rows = 0

        self.collect_size = 40 # size of the collectables for spacing
        self.collect_origin = [500, 1500] # origin from where to start placing collectables for frames
        self.collect_pos = self.collect_origin.copy() # the current position of collectable
        
        for index in np.ndindex(self.shape):
            # 1, 2 -> 50, 100 -> ??50, ?100
            pixel_origin = np.add(np.array(index) * self.pixel_size, self.pixel_origin)
            obj = self.level.create_object('box_generator', [
                *pixel_origin, 
                self.pixel_size / 2,
                self.pixel_size / 2, 
                0, -1, 0, -1, 6, 0, 0, # 0.1 dissapear    0 wait
                '\nnoanim'
            ])
            self.pixels[index] = obj.id

        self.level.create_object('start', [
            *self.collect_origin, 
            0.1, 0, 1 # size speed density
        ])
        self.level.create_object('collectable', [
            'i',
            *self.collect_origin,
            1,
            '\nzoomFactor -2'
            '\ntrigger',
            "\nsfx 'none'"
        ])

    def real_shape(self):
        #return tuple(np.array(self.shape) * self.pixel_size)
        #return tuple(np.multiply(self.shape, self.pixel_size))
        return tuple([x * self.pixel_size for x in self.shape])

    def add_frame(self, pixels):
        collect = self.level.create_object('collectable', [
            'isp',
            *self.collect_pos,
            1,
            '\ntrigger',
            "\nsfx 'none'"
        ])

        for pixel in pixels:
            index, state = pixel
            obj = self.level.get_object_by_id(self.pixels[index])
            if obj:
                self.level.create_object('special_connection', ['On' if state else 'Off'], [collect.id, obj.id])

        #if self.collect_pos[1] / self.collect_origin[1] == self.shape[1]:
        if self.pixel_rows > 10:
            og_pos = self.collect_pos.copy()
            self.collect_pos[1] = self.collect_origin[1]
            self.collect_pos[0] += self.collect_size
            self.pixel_rows = 0
            self.level.create_object('portal', [
                *og_pos,
                *self.collect_pos,
                1, 7, 0
            ])
        else:
            self.pixel_rows += 1
            self.collect_pos[1] += self.collect_size

def center_point(pos, shape): # center from origin
    return (pos[0] + shape[0] / 2, pos[1] + shape[1] / 2)

def inv_center_point(pos, shape): # origin from center
    return (pos[0] - shape[0] / 2, pos[1] - shape[1] / 2)

def image_to_bitmap(img, threshold=128):
    #img = Image.open(img).convert('L')
    img = Image.fromarray(np.array(img)).convert('L')
    img = img.point(lambda pixel: 0 if pixel < threshold else 1, mode='1')
    #img = np.array(img) > 0.5
    img = np.array(img, dtype=bool)
    return img

def loop_over_frames(vid, res, display):
    capture = cv2.VideoCapture(vid)

    frame_count = 0
    fps = 1
    previous_frame = np.zeros(shape=res, dtype=bool) # 0 = False = Black = On     1 = True = Black = Off

    print(f'Starting with {fps} FPS and {int(capture.get(cv2.CAP_PROP_FRAME_COUNT))} frames.')

    while capture.isOpened():
        ret, frame = capture.read()

        if not ret:
            break

        frame_count += 1
        if frame_count % (capture.get(cv2.CAP_PROP_FPS) / fps) == 0: # every nth frame
            print(f'Frame {frame_count}...', end=' ')
            resized = cv2.resize(frame, res)
            bitmap = image_to_bitmap(resized)
            bitmap = np.transpose(bitmap) # for some reason resolution and bitmap's shape are flipped
            pixels = []

            for index, value in np.ndenumerate(bitmap):
                if not previous_frame[index] and bitmap[index]:
                    pixels.append((index, True))
                    #display.set_pixel(*index, True)
                elif previous_frame[index] and not bitmap[index]:
                    pixels.append((index, False))
                    #display.set_pixel(*index, False)

            display.add_frame(pixels)
            previous_frame = bitmap.astype(bool)
            print('Done!')

    print('Finished processing all frames.')
    capture.release()
    cv2.destroyAllWindows()

def main():
    video_file_path, resolution, save_as_file = get_cli_args([
        { 'prompt': 'Video file path: ' },
        { 'prompt': 'Resolution (x,y): ', 'default': '12,6' },
        { 'prompt': 'Save as TXT file? (y/n) ', 'default': 'n' }
    ])
    resolution = string_to_tuple(resolution)
    #video_file_path, resolution, save_as_file = 'BadApple.mp4', (20, 10), 'y'

    level = Level()
    level.headers['gravity'] = [0.1, 270]
    level.headers['totalCircles'] = [7, 1]
    display = Display(level, resolution)
    loop_over_frames(video_file_path, resolution, display)
    level_text = level.stringify()

    level_output(level_text, save_as_file)

if __name__ == '__main__':
    main()
    #test()