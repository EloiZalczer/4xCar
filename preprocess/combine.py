#!/usr/bin/python

import sys, getopt, os
import numpy as np
from tqdm import tqdm

import h5py

filenames = ["combinednotmirrored.h5", "filteredlabelled.h5"]

def combine_hdf5():

    combined_images = []
    combined_commands = []

    for filename in filenames:
        hf = h5py.File(filename, 'r')

        images = hf.get('images')
        commands = hf.get('commands')

        images_np = np.array(images)
        commands_np = np.array(commands)

        for i in tqdm(range(len(images_np))):
            combined_images.append(images_np[i])
            combined_commands.append(commands_np[i])

        combined_images_np = np.array(combined_images)
        combined_commands_np = np.array(combined_commands)

        print(combined_images_np.shape)
        print(combined_commands_np.shape)

        hf = h5py.File("combined_new.h5", 'w')

        hf.create_dataset('images', data=combined_images_np.astype('uint8'))
        hf.create_dataset('commands', data=combined_commands_np)

        hf.close()


if __name__ == "__main__":

    combine_hdf5()
