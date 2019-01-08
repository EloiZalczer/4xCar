#!/usr/bin/python

import sys, getopt

DEFAULT_IP_ADDRESS = "192.168.1.1"

verbose = False
socket_address = DEFAULT_IP_ADDRESS

import torch

import picamera
import picamera.array

from threading import Thread

import numpy as np

import socketio

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
        else:
            assert False, "Unhandled option"


def acquire_image():

    # Acquire image from camera

    pass


def wait_commands():

    # Stop

    # Set max speed

    #Tweak parameters..

    pass

def launch_threads():
    camera_thread = Thread(target=acquire_image, args=())
    commands_thread = Thread(target=wait_commands, args=())

    camera_thread.start()
    commands_thread.start()


def autopilot():
    pass


if __name__ == '__main__':
    parse_args(sys.argv[1:])

    launch_threads()

    # Wait for start command

    # Start main loop
    autopilot()