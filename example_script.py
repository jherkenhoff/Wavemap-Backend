from measurement_controller import MeasurementController
from live_server import LiveServer
import random
import numpy as np

class ExampleController(MeasurementController):

    def get_device_info(self):
        return {
            "name": "Red Pitaya",
            "version": "1.8",
            "method": "FFT + Maxhold",
            "gps_support": False,
            "frequency_bins": np.logspace(6, 9, 1024).tolist()
        }

    def get_location(self):
        return {
            "lat": 53.06977 + random.uniform(-0.001, 0.001),
            "lon": 8.79107 + random.uniform(-0.001, 0.001),
            "alt": 5.71,
            "speed": None,
            "sats": 7,
            "accuracy": random.uniform(5, 30)
        }

    def get_spectrum(self):
        return [random.gauss(-130, 5) for i in range(len(self.get_device_info()["frequency_bins"]))]


if (__name__ == "__main__"):
    controller = ExampleController()
    server = LiveServer(controller)
    server.run()
