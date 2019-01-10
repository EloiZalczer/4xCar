#!/usr/bin/python

import sys, getopt

import torch

import picamera
import picamera.array

from threading import Thread, Event

import numpy as np

import socketio

DEFAULT_IP_ADDRESS = "http://localhost:3000"

verbose = False
manual_mode=False
socket_address = DEFAULT_IP_ADDRESS

direction = 0
speed = 0

start = Event()
stop = Event()
image_acquired = Event()

last_image = None

# Define function for verbose output
# verbose_print = None

def print_help():
    print("Usage : python3.6 main.py [-h|--help] [-v|--verbose] [-a|--address <ip_address>]")

def parse_args(args):

    global verbose, socket_address, manual_mode

    try:
        opts, args = getopt.getopt(args, "a:hv")
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
        else:
            assert False, "Unhandled option"


def acquire_image():

    # Acquire image from camera

    global last_image

    with picamera.PiCamera() as camera:
        while True:
            with picamera.array.PiRGBArray(camera) as output:
                camera.resolution = (200, 66)
                camera.capture(output, 'rgb')
                while(image_acquired.is_set()):
                    # Wait until last image has been processed to save it
                    pass
                last_image = output
                image_acquired.set()

def receive_commands():

    # Receive commands through websockets

    global direction, speed, max_speed

    socket = socketio.Client()

    @socket.on('command')
    def parse_command(command):
        verbose_print("Command received : ", command)
        direction = command['direction']
        speed = command['speed']

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
        max_speed = speed
        print("Setting max speed to ", max_speed)

    try:
        socket.connect(socket_address)
    except socketio.exceptions.ConnectionError:
        print("Could not connect to server. Exiting.")
	# sys.exit()

    socket.wait()

def launch_threads():

    verbose_print("Creating separate thread for image acquisition...")
    camera_thread = Thread(target=acquire_image, args=())
    camera_thread.start()
    verbose_print("Started")

    verbose_print("Creating separate thread for commands reception...")
    commands_thread = Thread(target=receive_commands, args=())
    commands_thread.start()
    verbose_print("Started")

def autopilot():
    # Auto pilot using pre-trained model

    print("Starting automatic pilot")

    start.wait()
    start.clear()

    print("Starting the car.")

    while True:
        if not stop.is_set():
            # Drive the car
            image_acquired.wait()
            #Process image then clear the event to go on to next image
            image_acquired.clear()
            pass
        else:
            print("Stopping the car.")
            start.wait()
            start.clear()
            stop.clear()
            print("Restarting the car.")

def manualpilot():
    print("Starting manual pilot")

    start.wait()
    start.clear()

    print("Starting the car.")

    while True:
        if not stop.is_set():
            # Drive the car

            pass
        else:
            print("Stopping the car.")
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

    launch_threads()

    print("System ready. Waiting for start.")
    # Wait for start command

    if not manual_mode:
        print("Starting autopilot")
        # Start main loop
        autopilot()
    else:
        print("Starting manual pilot")
        manualpilot()
