from ironcar.models.autopilot import DeepPicar

import numpy as np
from torch.autograd import Variable
from pytorch2keras.converter import pytorch_to_keras
import torch
import tensorflow as tf

from keras.layers import Lambda

def atan_layer(x):
    return tf.multiply(tf.atan(x), 2)

def atan_layer_shape(input_shape):
    return input_shape

input_np = np.random.uniform(0, 1, (1, 3, 200, 66))
input_var = Variable(torch.FloatTensor(input_np))

model = DeepPicar()

k_model = pytorch_to_keras(model, input_var, [(3, 200, 66)], verbose=True)

k_model.summary()

print(k_model)

k_model.add(Lambda(atan_layer, output_shape = atan_layer_shape, name = "atan_0"))

k_model.summary()