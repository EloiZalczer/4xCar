#!/usr/bin/python

import sys, getopt, os
import numpy as np
import cv2

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

    images_filtered = []
    commands_filtered = []

    for i in range(len(images_np)):
        image_title = "Dir : " + str(commands_np[i][0]) + " spd : " + str(commands_np[i][1])

        im = cv2.resize(images_np[i], (600, 198))

        cv2.imshow(image_title, im)

        key = cv2.waitKey(0)

        if key & 0xFF == ord('y'):
            images_filtered.append(images_np[i])
            commands_filtered.append(commands_np[i])

        print(i+1, "images processed")

        cv2.destroyAllWindows()

    images_filtered_np = np.array(images_filtered)
    commands_filtered_np = np.array(commands_filtered)

    hf = h5py.File("filtered.h5", 'w')

    hf.create_dataset('images', data=images_filtered_np.astype('uint8'))
    hf.create_dataset('commands', data=commands_filtered_np)

    hf.close()


if __name__ == "__main__":
    parse_args(sys.argv[1:])

    if use_most_recent:
        filename = get_most_recent_filename()

    print("Using file : ", filename)

    read_hdf5(filename)
