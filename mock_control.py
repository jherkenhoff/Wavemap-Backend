from control_backend import ControlBackend

class MockControl(ControlBackend):

    def get_device_info(self):
        return {
            "name": "Red Pitaya",
            "version": "1.8",
            "gps_support": False,
            "frequency_range": {
                "lower": 50e3,
                "upper": 2e6
            },
            "frequency_bins": 128
        }

    def get_location(self):
        pass

    def get_sample(self):
        pass


control = MockControl()
control.run()
