#!/usr/bin/python

import sys, getopt
import time

from pilot import AutoPilot, ManualPilot

import tensorflow as tf
from tensorflow import get_default_graph
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.utils import CustomObjectScope
from tensorflow.python.keras.initializers import glorot_uniform
# from keras.models import load_model
# from keras.utils import CustomObjectScope
# from keras.initializers import glorot_uniform

from threading import Thread, Event

import numpy as np

import socketio

import h5py

import serial

DEFAULT_IP_ADDRESS = "http://localhost:3000"
DEFAULT_SERIAL_ADDRESS = "/dev/ttyACM0"

verbose = False
manual_mode=False
serial_address = DEFAULT_SERIAL_ADDRESS
socket_address = DEFAULT_IP_ADDRESS

def print_help():
    print("Usage : python3.6 main.py [-h|--help] [-v|--verbose] [-a|--address <ip_address>]")

def parse_args(args):

    global verbose, serial_address, socket_address, manual_mode, to_hdf5

    try:
        opts, args = getopt.getopt(args, "a:s:hvm")
    except getopt.GetoptError as err:
        print(str(err))
        print_help()
        sys.exit()

    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            print_help()
            sys.exit()
        elif o in ("-a", "--address"):
            socket_address = a
        elif o in ("-m", "--manual"):
            manual_mode=True
        elif o in ("-s", "--serial"):
            serial_address = a
        else:
            assert False, "Unhandled option"

if __name__ == '__main__':
    parse_args(sys.argv[1:])

    if not manual_mode:
        pilot = AutoPilot(verbose, serial_address, socket_address)
    else:
        pilot = ManualPilot(verbose, serial_address, socket_address)
