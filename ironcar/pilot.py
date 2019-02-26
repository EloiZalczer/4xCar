#!/usr/bin/python

import socketio
from abc import ABC, abstractmethod
from threading import Event
import sys
import time
import serial
import numpy as np
import h5py

import tensorflow as tf
from tensorflow import get_default_graph
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.utils import CustomObjectScope
from tensorflow.python.keras.initializers import glorot_uniform

from camera import PiVideoStream


class Pilot(ABC):
    def __init__(self, verbose, serial_address, socket_address, max_speed=30):
        super().__init__()

        self.verbose_print = print if verbose else lambda *a, **k: None

        self.verbose_print("Using IP address ", socket_address)
        self.verbose_print("Using serial address ", serial_address)

        self.serial_address = serial_address
        self.socket_address = socket_address
        self.socket = socketio.Client()
        self.running = False
        self.startEvent = Event()
        self.stopEvent = Event()
        self.max_speed = max_speed
        self.ser = serial.Serial(serial_address, baudrate=115200, timeout=0)
        self.camera = PiVideoStream()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def init_socket(self):
        pass

    @abstractmethod
    def mainloop(self):
        pass


class AutoPilot(Pilot):
    def __init__(self,  verbose_print, serial_address, socket_address,
                 model_path='ironcar/models/keras_model_simplified_no_preprocess.h5',
                 max_speed=30):

        super().__init__(verbose_print, serial_address, socket_address, max_speed)
        self.model_path = model_path
        self.last_direction = 0

    def start(self):

        print("Starting automatic pilot")

        self.init_socket()

        self.verbose_print("Loading model from ", self.model_path)

        self.load_model()

        self.camera.start()

        self.mainloop()

    def init_socket(self):
        @self.socket.on('start')
        def start_car():
            print("Start signal received.")
            self.startEvent.set()

        @self.socket.on('stop')
        def stop_car():
            print("Stop signal received.")
            self.stopEvent.set()

        @self.socket.on('max_speed')
        def set_max_speed(speed):
            self.max_speed = speed
            print("Setting max speed to ", self.max_speed)

        try:
            self.socket.connect(self.socket_address)
        except socketio.exceptions.ConnectionError:
            print("Could not connect to server. Exiting.")
            sys.exit()

    def load_model(self):
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            self.model = load_model(self.model_path)
        self.graph = get_default_graph()

    def mainloop(self):

        self.startEvent.wait()
        self.startEvent.clear()

        print("Starting the car.")

        while True:
            if not self.stopEvent.is_set():

                start_time = time.time()

                input = self.camera.read_processed()

                with self.graph.as_default():
                    pred = self.model.predict(input)

                # Si la direction inferee est trop differente de celle actuelle, on la moyenne avec la precedente pour
                # limiter les effets des predictions aberrantes

                direction = int(np.round(pred[0][0] * 30))
                if direction > self.last_direction+20 or direction < self.last_direction - 20:
                    direction = self.last_direction + direction / 2

                self.verbose_print("Command from network : ", direction)
                speed = 1
                self.ser.write(bytes([direction + 90, speed + 90, 0]))

                self.last_direction = direction

                self.verbose_print("Time for one iteration : ", time.time() - start_time)
            else:
                print("Stopping the car.")
                self.ser.write(bytes([90, 90, 0]))
                self.startEvent.wait()
                self.startEvent.clear()
                self.stopEvent.clear()
                print("Restarting the car.")


class ManualPilot(Pilot):

    def __init__(self, verbose_print, serial_address, socket_address, framerate=20, max_speed=30):
        super().__init__(verbose_print, serial_address, socket_address, max_speed)
        self.recording = False
        self.running = False
        self.commands = []
        self.images = []
        self.direction = 0
        self.speed = 0
        self.framerate = framerate
        self.camera.start()

    def start(self):
        print("Starting manual pilot")

        self.init_socket()

        self.mainloop()

    def init_socket(self):

        @self.socket.on('command')
        def parse_command(command):
            if self.running:
                self.verbose_print("Command received : ", command)
                self.direction = command['direction']
                self.speed = command['speed']
                self.ser.write(bytes([self.direction + 90, self.speed + 90, 0]))

        @self.socket.on('start')
        def start_car():
            print("Start signal received.")
            self.startEvent.set()
            self.running = True

        @self.socket.on('stop')
        def stop_car():
            print("Stop signal received.")
            self.stopEvent.set()
            self.direction = 0
            self.speed = 0
            self.ser.write(bytes([self.direction + 90, self.speed + 90, 0]))
            self.running = False

        @self.socket.on('max_speed')
        def set_max_speed(speed):
            self.max_speed = speed
            print("Setting max speed to ", self.max_speed)

        @self.socket.on('start_record')
        def start_record():
            self.recording = True

        @self.socket.on('stop_record')
        def stop_record():
            self.recording = False

        try:
            self.socket.connect(self.socket_address)
        except socketio.exceptions.ConnectionError:
            print("Could not connect to server. Exiting.")
            sys.exit()

    def mainloop(self):
        print("Starting manual pilot")

        self.startEvent.wait()
        self.startEvent.clear()

        print("Starting the car.")

        while True:
            if self.stopEvent.is_set():
                print("Stopping the car.")
                self.save_hdf5()
                self.images = []
                self.commands = []
                self.startEvent.wait()
                self.startEvent.clear()
                self.stopEvent.clear()
                print("Restarting the car.")
            else:
                if self.recording:
                    self.images.append(self.camera.read())
                    self.commands.append((self.direction, self.speed))
                    time.sleep(.25)

    def save_hdf5(self):

        if len(self.commands) == 0:
            return

        filename = time.strftime("%Y%m%d%H%M%S") + ".h5"

        self.verbose_print("Saving data to", filename)

        hf = h5py.File(filename, 'w')

        images_np = np.array(self.images)
        commands_np = np.array(self.commands)

        hf.create_dataset('images', data=images_np)
        hf.create_dataset('commands', data=commands_np)

        hf.close()

        self.verbose_print("Done")
