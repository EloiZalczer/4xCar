import getopt
import sys

import h5py
import numpy as np

filename = None

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


def augment():
    hf = h5py.File(filename, 'r')

    commands = hf.get('commands')

    commands_np = np.array(commands)

    mean = np.mean(commands_np)
    q1 = np.percentile(commands_np, 25)
    median = np.percentile(commands_np, 50)
    q3 = np.percentile(commands_np, 75)

    right = np.count_nonzero(commands_np < 0)
    left = np.count_nonzero(commands_np > 0)

    print("Data mean : ", mean)
    print("First quartile : ", q1)
    print("Data median : ", median)
    print("Third quartile : ", q3)

    print(right, "images going right")
    print(left, "images going left")

    hf.close()

if __name__ == "__main__":
    parse_args(sys.argv[1:])

    augment()