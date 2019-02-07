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


def convert_bw():
    hf = h5py.File(filename, 'r')

    images = hf.get('images')
    commands = hf.get('commands')

    images_np = np.array(images)
    commands_np = np.array(commands)

    print(images_np.shape)

    images_bw = np.empty(shape=(images_np.shape[0], images_np.shape[1], images_np.shape[2], 1))

    for i in tqdm(range(len(images_np))):
        images_bw[i] = np.expand_dims(cv2.cvtColor(images_np[i], cv2.COLOR_RGB2GRAY),  axis=3)

    new_filename = time.strftime("%Y%m%d%H%M%S") + ".h5"

    hf = h5py.File(new_filename, 'w')

    hf.create_dataset('images', data=images_bw)
    hf.create_dataset('commands', data=commands_np)

    hf.close()

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    convert_bw()