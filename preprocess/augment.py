import h5py
import numpy as np
import cv2
import sys, getopt
from tqdm import tqdm
import time

import cv2

filename = None

def parse_args(args):
    global filename

    try:
        opts, args = getopt.getopt(args, "i:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit()

    for o, a in opts:
        if o in ("-i", "--input"):
            filename = a
        else:
            assert False, "Unhandled option"


def augment():
    hf = h5py.File(filename, 'r')

    images = hf.get('images')
    commands = hf.get('commands')

    images_np = np.array(images)
    commands_np = np.array(commands)

    print(images_np.shape)

    for i in tqdm(range(len(images_np))):
        new_cmd = commands_np[i]*1.4
        if new_cmd>30:
            new_cmd=30
        elif new_cmd<-30:
            new_cmd=-30

        commands_np[i] = new_cmd

    new_filename = filename.split('.')[0] + "augmented.h5"

    hf = h5py.File(new_filename, 'w')

    hf.create_dataset('images', data=images_np)
    hf.create_dataset('commands', data=commands_np)

    hf.close()

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    augment()