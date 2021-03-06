#!/usr/bin/python

import h5py
import numpy as np
import cv2
import sys, getopt
from matplotlib import pyplot as plt
from tqdm import tqdm
import time

filename = None


class Preprocessor:
    def __init__(self, filename, save_after_filter=True):
        self.hf = h5py.File(filename, 'r')

        self.images = self.hf.get('images')
        self.commands = self.hf.get('commands')

        self.images_np = np.array(self.images)
        self.commands_np = np.array(self.commands)

        self.save_after_filter = save_after_filter

        self.filters = []

    def add(self, filter):
        self.filters.append(filter)

    def run(self):

        for filter in self.filters:
            filtered_images, commands = filter.process(np.copy(self.images_np), np.copy(self.commands_np))
            if self.save_after_filter:
                self.images_np = np.concatenate((self.images_np, filtered_images), axis=0)
                self.commands_np = np.concatenate((self.commands_np, commands), axis=0)
            else:
                self.images_np = filtered_images
                self.commands_np = commands

        print("Taille : ", self.images_np.shape)

        self.save_hdf5()

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

        hf.create_dataset('images', data=self.images_np.astype('uint8'))
        hf.create_dataset('commands', data=self.commands_np)

        hf.close()


class Exposure:
    def __init__(self, contrast, brightness):
        self.brightness = brightness
        self.contrast = contrast

    def process(self, images, commands):

        print("Adding Exposure Variations")

        for i in tqdm(range(len(images))):
            images[i] = cv2.convertScaleAbs(images[i], alpha=np.random.uniform(1/self.contrast, self.contrast),
                                            beta=np.random.uniform(-1, 1)*self.brightness)

        return images, commands


class Crop:
    def __init__(self, proportion):
        self.proportion = proportion

    def process(self, images, commands):

        print("Cropping images")

        for i in tqdm(range(len(images))):

            dimX = np.around((1 - self.proportion)*images[i].shape[1]).astype("uint8")
            dimY = np.around((1 - self.proportion)*images[i].shape[0]).astype("uint8")

            startX = np.around(np.random.uniform()*self.proportion*images[i].shape[1]).astype("uint8")
            startY = np.around(np.random.uniform()*self.proportion*images[i].shape[0]).astype("uint8")

            tmp_image = images[i][startX:startX+dimX, startY:startY+dimY]
            images[i] = cv2.resize(tmp_image,(images[i].shape[1],images[i].shape[0]))

        return images, commands


class Obstacle:
    def __init__(self, max_X, max_Y):
        self.max_X = max_X
        self.max_Y = max_Y

    def process(self, images, commands):

        print("Adding Obstacles")

        for i in tqdm(range(len(images))):
            dimX = np.around(np.random.uniform() * self.max_X).astype("uint8")
            dimY = np.around(np.random.uniform() * self.max_Y).astype("uint8")

            startX = np.around(np.random.uniform() * (images[i].shape[1] - dimX)).astype("uint8")
            startY = np.around(np.random.uniform() * (images[i].shape[0] - dimY)).astype("uint8")

            images[i][startX:startX+dimX, startY:startY+dimY] = 0

        return images, commands


class GaussianNoise:
    def __init__(self, var):
        self.var = var

    def process(self, images, commands):

        print("Adding Gaussian Noise")

        for i in tqdm(range(len(images))):
            row, col, ch = images[i].shape
            mean = 0
            sigma = self.var ** 0.5
            gauss = np.random.normal(mean, sigma, (row, col, ch))
            gauss = gauss.reshape(row, col, ch)
            images[i] = np.clip(images[i] + gauss, 0, 255)

        return images, commands


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

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    preprocessor = Preprocessor(filename)

    preprocessor.add(Exposure(1.25, 15))
    # preprocessor.add(Crop(0.05))
    preprocessor.add(GaussianNoise(1))

    preprocessor.run()

