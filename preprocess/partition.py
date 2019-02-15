import h5py
import numpy as np
import sys, getopt
from tqdm import tqdm

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


def partition():
    hf = h5py.File(filename, 'r')

    images = hf.get('images')
    commands = hf.get('commands')

    images_np = np.array(images)
    commands_np = np.array(commands)

    print(images_np.shape)

    images_train = []
    commands_train = []

    images_val = []
    commands_val = []

    for i in tqdm(range(len(images_np))):
        r = np.random.uniform()
        if r < (1/6):
            images_val.append(images_np[i])
            commands_val.append(commands_np[i])
        else:
            images_train.append(images_np[i])
            commands_train.append(commands_np[i])

    filename_train = filename + "_train.h5"

    filename_val = filename + "_val.h5"

    images_train_np = np.array(images_train)
    commands_train_np = np.array(commands_train)

    print("Train set size : ", images_train_np.shape)

    images_val_np = np.array(images_val)
    commands_val_np = np.array(commands_val)

    print("Validation set size : ", images_val_np.shape)

    hf = h5py.File(filename_train, 'w')

    hf.create_dataset('images', data=images_train_np.astype('uint8'))
    hf.create_dataset('commands', data=commands_train_np)

    hf.close()

    hf = h5py.File(filename_val, 'w')

    hf.create_dataset('images', data=images_val_np.astype('uint8'))
    hf.create_dataset('commands', data=commands_val_np)

    hf.close()

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    partition()