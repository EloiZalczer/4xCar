#!/usr/bin/python

import sys, getopt, os
import numpy as np
from tqdm import tqdm

import h5py

filenames = ["from_generator_test.h5", "20190211112835.h5"]

def combine_hdf5():

    combined_images = np.empty(shape=(0, 66, 200, 3))
    combined_commands = np.empty(shape=(0, 2))

    for filename in filenames:
        hf = h5py.File(filename, 'r')

        images = hf.get('images')
        commands = hf.get('commands')

        images_np = np.array(images)
        commands_np = np.array(commands)

        print(images_np.shape)
        print(combined_images.shape)

        combined_images = np.append(combined_images, images_np, axis=0)
        combined_commands = np.append(combined_commands, commands_np, axis=0)

        print(combined_images.shape)
        print(combined_commands.shape)


if __name__ == "__main__":

    combine_hdf5()
