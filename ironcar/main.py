#!/usr/bin/python

import sys, getopt
import time

import torch

import picamera
import picamera.array

from enum import Enum

from PIL import Image

from threading import Thread, Event

import numpy as np

import socketio

import h5py

DEFAULT_IP_ADDRESS = "http://localhost:3000"
CAMERA_RESOLUTION = (200, 66)

class Direction(Enum):
    FULL_AHEAD = 1
    FULL_RIGHT = 2
    FULL_LEFT = 3
    HALF_RIGHT = 4
    HALF_LEFT = 5

class Speed(Enum):
    STOP = 1
    HALF_SPEED = 2
    FULL_SPEED = 3

verbose = False
manual_mode=False
socket_address = DEFAULT_IP_ADDRESS
train = False
commands = []
images = []
direction = Direction.FULL_AHEAD
speed = Speed.STOP

start = Event()
stop = Event()
image_acquired = Event()
record = Event()
record.set()

last_image = None

# Define function for verbose output
# verbose_print = None

def print_help():
    print("Usage : python3.6 main.py [-h|--help] [-v|--verbose] [-a|--address <ip_address>]")

def parse_args(args):

    global verbose, socket_address, manual_mode, to_hdf5

    try:
        opts, args = getopt.getopt(args, "a:hvmt")
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
        else:
            assert False, "Unhandled option"


def acquire_image():

    # Acquire image from camera

    global last_image, direction, speed, commands, images
    i = 0

    camera = picamera.PiCamera(framerate=60)
    camera.resolution = CAMERA_RESOLUTION
    output = picamera.array.PiRGBArray(camera, size=CAMERA_RESOLUTION)
    stream = camera.capture_continuous(output, format="rgb", use_video_port=True)

    for f in stream:
        while image_acquired.is_set():
            pass
        last_image = output
        image_acquired.set()
        # filename = str(i)+".png"
        # img_arr = f.array
        # img = Image.fromarray(img_arr)
        # img.save(filename)
        # verbose_print(filename, " saved to drive.")
        verbose_print("Image acquired : ", i)
        i += 1
        output.truncate(0)
        if record.is_set():
            images.append(last_image.array)
            print("Direction : ", direction, " speed : ", speed)
            commands.append((direction.value, speed.value))

def round_direction(direction):
    if direction < -5:
        if direction < -20:
            return Direction.FULL_LEFT
        return Direction.HALF_LEFT
    elif direction > 5:
        if direction > 20:
            return Direction.FULL_RIGHT
        return Direction.HALF_RIGHT
    return Direction.FULL_AHEAD

def round_speed(speed):
    if speed > 5:
        if speed > 20:
            return Speed.FULL_SPEED
        return Speed.HALF_SPEED
    return Speed.STOP

def receive_commands():

    # Receive commands through websockets

    socket = socketio.Client()

    @socket.on('command')
    def parse_command(command):

        global direction, speed
        verbose_print("Command received : ", command)
        direction = round_direction(command['direction'])
        speed = round_speed(command['speed'])

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
        # sys.exit()

def start_camera():
    verbose_print("Creating separate thread for image acquisition...")
    camera_thread = Thread(target=acquire_image, args=())
    camera_thread.start()
    verbose_print("Started")

def autopilot():
    # Auto pilot using pre-trained model

    print("Starting automatic pilot")

    start.wait()
    start.clear()

    print("Starting the car.")

    while True:
        if not stop.is_set():
            image_acquired.wait()
            # Drive the car
            print("Driving the car")
            #Process image then clear the event to go on to next image

            image_acquired.clear()
            pass
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
        if not stop.is_set():
            # Drive the car
            image_acquired.wait()
            print("Driving in manual mode")
            image_acquired.clear()
            pass
        else:
            print("Stopping the car.")
            save_hdf5()
            start.wait()
            start.clear()
            stop.clear()
            print("Restarting the car.")

if __name__ == '__main__':
    parse_args(sys.argv[1:])

    verbose_print = print if verbose else lambda *a, **k: None

    print("Verbose : ", verbose)

    print("Verbose print : ", verbose_print)

    verbose_print("Using IP address ", socket_address)

    start_camera()

    receive_commands()

    print("System ready. Waiting for start.")
    # Wait for start command

    if not manual_mode:
        print("Starting autopilot")
        # Start main loop
        autopilot()
    else:
        print("Starting manual pilot")
        manualpilot()
