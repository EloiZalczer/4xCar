from PIL import Image
import numpy as np
from os import listdir
from matplotlib import pyplot as plt
import h5py
from tqdm import tqdm

images = ["dataset/"+x for x in listdir("dataset")]
images_np = []
commands = []

for image in tqdm(images):
    pic = Image.open(image)
    numpy_pic = np.array(pic)

    direction = float(image.split('_')[5][0:-4])
    direction = round(direction*15, 0)
    if direction > 30:
        direction = 30
    elif direction < -30:
        direction = -30

    commands.append(direction)
    images_np.append(numpy_pic)

hf = h5py.File("from_generator_test.h5", 'w')
img = np.array(images_np)
cmd = np.array(commands)

hf.create_dataset("images", data=img)
hf.create_dataset("commands", data=cmd)

hf.close()

