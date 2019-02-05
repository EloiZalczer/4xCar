#!/usr/bin/python

import h5py
import numpy as np
import cv2
import sys, getopt, os
from matplotlib import pyplot as plt
import time

filename = None

class Preprocessor():
    def __init__(self, filename, save_after_filter=True, shuffle=True):
        self.hf = h5py.File(filename, 'r')

        self.images = self.hf.get('images')
        self.commands = self.hf.get('commands')

        self.images_np = np.array(self.images)
        self.commands_np = np.array(self.commands)

        self.save_after_filter = save_after_filter

        self.shuffle = shuffle

        self.filters = []

    def add(self, filter):
        self.filters.append(filter)

    def run(self):

        for filter in self.filters:
            filtered_images, commands = filter.process(np.copy(self.images_np), np.copy(self.commands_np.copy()))
            print("Image np 0 : ", self.images_np[0])
            print("Filtered image 0 : ", filtered_images[0])
            if self.save_after_filter:
                self.images_np = np.append(self.images_np, filtered_images, axis=0)
                self.commands_np = np.append(self.commands_np, commands, axis=0)
            else:
                self.images_np = filtered_images
                self.commands_np = commands

            print("Shape images : ", self.images_np.shape)
            print("Shape commands : ", self.commands_np.shape)

        print(self.images_np[0])
        print(self.commands_np[0])

        print("Shape images : ", self.images_np.reshape(len(self.images_np), -1).shape)
        print("Shape commands : ", self.commands_np.reshape(len(self.commands_np), -1).shape)

        self.data = np.c_[
            self.images_np.reshape(len(self.images_np), -1), self.commands_np.reshape(len(self.commands_np), -1)].astype("int")

        if self.shuffle:
            np.random.shuffle(self.data)

        self.images_np = self.data[:, :self.images_np.size//len(self.images_np)].reshape(self.images_np.shape)
        self.commands_np = self.data[:, self.images_np.size//len(self.images_np):].reshape(self.commands_np.shape)

        self.disp_random()

        print("Taille : ", self.images_np.shape)

        # self.save_hdf5()

    def disp_random(self):
        for i in range(10):

            index = np.random.randint(0, len(self.images_np))
            plt.figure()
            plt.imshow(self.images_np[index])
            plt.show()
            print("Direction : ", self.commands_np[index][0], ", vitesse : ", self.commands_np[index][1])

    def save_hdf5(self):
        filename = time.strftime("%Y%m%d%H%M%S") + ".h5"

        hf = h5py.File(filename, 'w')

        hf.create_dataset('images', data=self.images_np)
        hf.create_dataset('commands', data=self.commands_np)

        hf.close()

class Exposure():
    def __init__(self, contrast, brightness):
        self.brightness = brightness
        self.contrast = contrast

    def process(self, images, commands):
        for i in range(len(images)):
            images[i] = cv2.convertScaleAbs(images[i], alpha=np.random.uniform(1/self.contrast, self.contrast),
                                            beta=np.random.uniform(-1, 1)*self.brightness)

            # print(images[i])

        return images, commands


class Crop():
    def __init__(self, proportion):
        self.proportion = proportion

    def process(self, images, commands):
        for i in range(len(images)):

            # print("Shape : ", images[i].shape)

            dimX = np.around((1 - self.proportion)*images[i].shape[1]).astype("int")
            dimY = np.around((1 - self.proportion)*images[i].shape[0]).astype("int")

            startX = np.around(np.random.uniform()*self.proportion*images[i].shape[1]).astype("int")
            startY = np.around(np.random.uniform()*self.proportion*images[i].shape[0]).astype("int")

            # print("StartX", startX, "StartY", startY, "dimX", dimX, "dimY", dimY)

            tmp_image = images[i][startX:startX+dimX, startY:startY+dimY]
            images[i] = cv2.resize(tmp_image,(images[i].shape[1],images[i].shape[0]))

        return images, commands


class Obstacle():
    def __init__(self, max_X, max_Y):
        self.max_X = max_X
        self.max_Y = max_Y

    def process(self, images, commands):
        for i in range(len(images)):
            dimX = np.around(np.random.uniform() * self.max_X).astype("int")
            dimY = np.around(np.random.uniform() * self.max_Y).astype("int")

            # print("DimX : ", dimX)
            # print("DimY : ", dimY)

            startX = np.around(np.random.uniform() * (images[i].shape[1] - dimX)).astype("int")
            startY = np.around(np.random.uniform() * (images[i].shape[0] - dimY)).astype("int")

            # print("StartX : ", startX)
            # print("StartY : ", startY)

            images[i][startX:startX+dimX, startY:startY+dimY] = 0

        return images, commands


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

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    preprocessor = Preprocessor(filename)

    preprocessor.add(Exposure(1.5, 30))
    preprocessor.add(Crop(0.05))
    preprocessor.add(Obstacle(100, 50))

    preprocessor.run()

