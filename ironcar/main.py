#!/usr/bin/python

import sys, getopt

import torch

# import picamera
# import picamera.array

from threading import Thread

import numpy as np

import socketio

DEFAULT_IP_ADDRESS = "192.168.1.1"

verbose = False
manual_mode=False
socket_address = DEFAULT_IP_ADDRESS

direction = 0
speed = 0

# Define function for verbose output
verbose_print = print if verbose else lambda *a, **k: None

def print_help():
    print("Usage : python3.6 main.py [-h|--help] [-v|--verbose] [-a|--address <ip_address>]")

def parse_args(args):
    try:
        opts, args = getopt.getopt(args, "a:hv")
    except getopt.GetoptError as err:
        print(str(err))
        print_help()
        sys.exit(2)

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

    pass

def launch_threads():

    verbose_print("Creating separate thread for image acquisition...")
    camera_thread = Thread(target=acquire_image, args=())
    camera_thread.start()
    verbose_print("Started")


def autopilot():
    # Auto pilot using pre-trained model
    pass

def manualpilot():
    # Manual pilot based on received commands
    pass

if __name__ == '__main__':
    parse_args(sys.argv[1:])

    verbose_print("Using IP address ", socket_address)

    launch_threads()

    socket = socketio.Client()

    @socket.on('command')
    def parse_command(command):
        print("Command : ", command)

    socket.connect("http://localhost:3000")

    print("System ready. Waiting for start.")
    # Wait for start command

    socket.wait()

    if not manual_mode:
        print("Starting autopilot")
        # Start main loop
        autopilot()
    else:
        print("Starting manual pilot")
        manualpilot()