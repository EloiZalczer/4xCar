#!/usr/bin/python

import sys, getopt

from pilot import AutoPilot, ManualPilot

DEFAULT_IP_ADDRESS = "http://localhost:3000"
DEFAULT_SERIAL_ADDRESS = "/dev/ttyACM0"

verbose = False
manual_mode = False
serial_address = DEFAULT_SERIAL_ADDRESS
socket_address = DEFAULT_IP_ADDRESS


def print_help():
    print("Usage : python3.6 main.py [-h|--help] [-v|--verbose] [-a|--address <ip_address>]")


def parse_args(args):

    global verbose, serial_address, socket_address, manual_mode

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
            manual_mode = True
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

    pilot.start()
