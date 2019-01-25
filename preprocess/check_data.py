#!/usr/bin/python

import sys, getopt, os
import numpy as np
from matplotlib import pyplot as plt

import h5py

use_most_recent = True
filename = None

def parse_args(args):

    global use_most_recent, filename
    
    try:
        opts, args = getopt.getopt(args, "i:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit()

    for o, a in opts:
        if o in ("-i", "--input"):
            use_most_recent = False
            filename = a
        else:
            assert False, "Unhandled option"

def get_most_recent_filename():
    most_recent_date = 0
    most_recent_file = ""
    for filename in os.listdir(path='/home/eloi/Documents/PFE/'):
            print("Filename : ", filename)
            if ".h5" in filename:
                date = int(filename.split('.')[0])
                if(date>most_recent_date):
                    most_recent_file = filename
                    most_recent_date = date

    return most_recent_file
            
def read_hdf5(filename):
    hf = h5py.File(filename, 'r')

    images = hf.get('images')
    commands = hf.get('commands')

    images_np = np.array(images)
    print(len(images_np))
    commands_np = np.array(commands)

    for i in range(700, len(images_np)):
        #if commands_np[i][0] != 0:
        plt.figure()
        plt.imshow(images_np[i])
        plt.show()
        print("Direction : ", commands_np[i][0], " speed : ", commands_np[i][1])

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    if use_most_recent:
        filename = get_most_recent_filename()

    print("Using file : ", filename)

    read_hdf5(filename)
