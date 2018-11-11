from threading import Thread, Event
from enum import Enum
import time

class MeasurementMode(Enum):
    SINGLE     = 1
    CONTINUOUS = 2

class MeasurementThread(Thread):
    def __init__(self, emit, measurement_script):
        super().__init__()

        self.__emit = emit
        self.__measurement_script = measurement_script

        # Initialize internal state
        self.__mode = MeasurementMode.SINGLE
        self.__delay = 1.0

        # Setup events:
        self.__run_event = Event()

    def start_single(self):
        self.__mode = MeasurementMode.SINGLE
        self.__run_event.set()

    def start_continuous(self, delay):
        self.__delay = delay
        self.__mode = MeasurementMode.CONTINUOUS
        self.__run_event.set()

    def stop_continuous(self):
        self.__run_event.clear()

    def run(self):
        while self.__run_event.wait():
            if (self.__mode == MeasurementMode.SINGLE):
                sample = {
                    "id": 0,
                    "time": "22:57:53",
                    "rf_power": -82,
                    "spectrum": self.__measurement_script.get_spectrum(),
                    "location": self.__measurement_script.get_location()
                }
                self.__emit("new_sample", sample, broadcast=True)
                self.__run_event.clear()
            elif (self.__mode == MeasurementMode.CONTINUOUS):
                sample = {
                    "id": 0,
                    "time": "22:57:53",
                    "rf_power": -82,
                    "spectrum": self.__measurement_script.get_spectrum(),
                    "location": self.__measurement_script.get_location()
                }
                self.__emit("new_sample", sample, broadcast=True)
                time.sleep(self.__delay)
