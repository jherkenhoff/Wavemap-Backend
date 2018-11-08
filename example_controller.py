from controller_backend import ControllerBackend
import random

class ExampleController(ControllerBackend):

    def get_device_info(self):
        return {
            "name": "Red Pitaya",
            "version": "1.8",
            "method": "FFT + Maxhold",
            "gps_support": False,
            "frequency_bins": [50e6, 60e6, 70e6],
            "custom_fileds": {
            }
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
        return [-90, -80, -91]

if (__name__ == "__main__"):
    controller = ExampleController()
    controller.run()
