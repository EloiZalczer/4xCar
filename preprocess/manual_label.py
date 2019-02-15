#!/usr/bin/python

import sys, getopt, os
import numpy as np
import cv2

import h5py

filename = None

line_start = None
line_end = None
new_label = None

def on_mouse(event, x, y, flags, params):

    global line_start, line_end, new_label

    if event == cv2.EVENT_LBUTTONDOWN:
        line_start = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        line_end = (x, y)

        len1 = line_end[0]-line_start[0]
        len2 = line_end[1]-line_start[1]

        res = round((len1/len2)*15)

        if res < -30:
            res = -30
        elif res > 30:
            res = 30

        print("New label : ", res)
        new_label = res

def parse_args(args):
    global use_most_recent, filename

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

def label_hdf5(filename):

    global processed, new_label

    hf = h5py.File(filename, 'r')

    images = hf.get('images')

    images_np = np.array(images)
    print(len(images_np), "total images in file.")

    images_labeled = []
    commands_labeled = []

    for i in range(len(images_np)):

        title = "Image " + str(i)

        im = cv2.resize(images_np[i], (600, 198))

        cv2.namedWindow(title)
        cv2.setMouseCallback(title, on_mouse, 0)
        cv2.imshow(title, im)

        cv2.waitKey(0)

        images_labeled.append(images_np[i])
        commands_labeled.append(new_label)

        print(i + 1, "images processed")

        cv2.destroyAllWindows()

    images_labeled_np = np.array(images_labeled)
    commands_labeled_np = np.array(commands_labeled)

    new_filename = filename.split('.')[0] + "labelled.h5"

    hf = h5py.File(new_filename, 'w')

    hf.create_dataset('images', data=images_labeled_np.astype('uint8'))
    hf.create_dataset('commands', data=commands_labeled_np)

    hf.close()


if __name__ == "__main__":
    parse_args(sys.argv[1:])

    print("Using file : ", filename)

    label_hdf5(filename)