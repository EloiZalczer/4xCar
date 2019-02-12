import h5py
import numpy as np
import cv2
import sys, getopt
from tqdm import tqdm
import time

import cv2

axis=1
filename = None

def parse_args(args):
    global filename, axis

    try:
        opts, args = getopt.getopt(args, "i:h")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit()

    for o, a in opts:
        if o in ("-i", "--input"):
            filename = a
        elif o in ("-h", "--horizontal"):
            axis = 0
        else:
            assert False, "Unhandled option"


def mirror():
    hf = h5py.File(filename, 'r')

    images = hf.get('images')
    commands = hf.get('commands')

    images_np = np.array(images)
    commands_np = np.array(commands)

    print(images_np.shape)

    images_mirrored = np.empty(shape=images_np.shape)
    commands_mirrored = np.empty(shape=commands_np.shape)

    for i in tqdm(range(len(images_np))):
        images_mirrored[i] = cv2.flip(images_np[i], axis)
        commands_mirrored[i][1] = commands_np[i][1]
        if axis == 1:
            commands_mirrored[i][0] = -commands_np[i][0]
        else:
            commands_mirrored[i][0] = commands_np[i][0]

    hf = h5py.File("mirrored.h5", 'w')

    hf.create_dataset('images', data=images_mirrored.astype('int'))
    hf.create_dataset('commands', data=commands_mirrored)

    hf.close()

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    mirror()