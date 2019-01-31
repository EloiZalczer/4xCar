#!/usr/bin/python

import sys, getopt
import time

from camera import PiVideoStream

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
socket_address = DEFAULT_IP_ADDRESS
serial_address = DEFAULT_SERIAL_ADDRESS

commands = []
images = []
ser = None

direction = 0
speed = 0

start = Event()
stop = Event()
record = Event()

# Define function for verbose output
# verbose_print = None

def print_help():
    print("Usage : python3.6 main.py [-h|--help] [-v|--verbose] [-a|--address <ip_address>]")

def parse_args(args):

    global verbose, serial_address, socket_address, manual_mode, to_hdf5

    try:
        opts, args = getopt.getopt(args, "a:s:hvmt")
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
        elif o in ("-t", "--train"):
            train=True
        elif o in ("-s", "--serial"):
            serial_address = a
        else:
            assert False, "Unhandled option"

def receive_commands():

    # Receive commands through websockets

    socket = socketio.Client()

    @socket.on('command')
    def parse_command(command):

        global direction, speed
        
        verbose_print("Command received : ", command)
        direction = command['direction']
        speed = command['speed']
        ser.write(bytes([direction+90, speed+90, 0]))

    @socket.on('start')
    def start_car():
        print("Start signal received.")
        start.set()

    @socket.on('stop')
    def stop_car():
        print("Stop signal received.")
        stop.set()

    @socket.on('max_speed')
    def set_max_speed(speed):

        global max_speed
        
        max_speed = speed
        print("Setting max speed to ", max_speed)

    @socket.on('start_record')
    def start_record():
        record.set()

    @socket.on('stop_record')
    def stop_record():
        record.clear()

    try:
        socket.connect(socket_address)
    except socketio.exceptions.ConnectionError:
        print("Could not connect to server. Exiting.")
        sys.exit()

def autopilot():
    # Auto pilot using pre-trained model

    print("Starting automatic pilot")

    start.wait()
    start.clear()

    global direction, speed

    verbose_print("Loading model")

    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model('ironcar/models/keras_model_no_preprocess.h5')
    graph = get_default_graph()

    print("Starting the car.")

    while True:
        if not stop.is_set():

            start_time = time.time()

            input = camera.read()

            with graph.as_default():
                pred = model.predict(input)

            print(pred[0])
            direction = int(np.round(pred[0][0]*30))

            verbose_print("Command from network : ", direction)
            speed = 1
            ser.write(bytes([direction+90, speed+90, 0]))

            print("Time for one iteration : ", time.time()-start_time)
        else:
            print("Stopping the car.")
            start.wait()
            start.clear()
            stop.clear()
            print("Restarting the car.")

def save_hdf5():

    global commands, images

    if len(commands) == 0:
        return

    filename = time.strftime("%Y%m%d%H%M%S") + ".h5"

    hf = h5py.File(filename, 'w')

    images_np = np.array(images)
    commands_np = np.array(commands)
    
    hf.create_dataset('images', data = images_np)
    hf.create_dataset('commands', data = commands_np)

    hf.close()

def manualpilot():
    print("Starting manual pilot")

    start.wait()
    start.clear()

    print("Starting the car.")

    while True:
        if stop.is_set():
            print("Stopping the car.")
            save_hdf5()
            start.wait()
            start.clear()
            stop.clear()
            print("Restarting the car.")
        else:
            if (record.is_set()):
                images.append(camera.read())
                commands.append((direction, speed))

if __name__ == '__main__':
    parse_args(sys.argv[1:])

    verbose_print = print if verbose else lambda *a, **k: None

    print("Verbose : ", verbose)

    print("Verbose print : ", verbose_print)

    verbose_print("Using IP address ", socket_address)

    camera = PiVideoStream()
    camera.start()

    receive_commands()

    ser = serial.Serial(serial_address, baudrate=115200, timeout=0)

    print("System ready. Waiting for start.")
    # Wait for start command

    if not manual_mode:
        print("Starting autopilot")
        # Start main loop
        autopilot()
    else:
        print("Starting manual pilot")
        manualpilot()
