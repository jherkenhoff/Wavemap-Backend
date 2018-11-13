from abc import ABC, abstractmethod

class MeasurementController(ABC):

    def __init__(self):
        pass

    ############################################################################
    # REQUIRED METHODS
    ############################################################################

    @abstractmethod
    def get_device_info(self):
        """Returns devices metadata.

        This method is REQUIRED and must be implemented by the derived class.

        The return value should contain a dict with information about the measuring-device.
        The following fields are MANDATORY: name, version, method, gps_support, frequency_bins.

        You may provide additional fields to uniquely identify your device.

        The following statement shows a minimal example that satisfies the requirements:

        return {
            "name": "Red Pitaya",
            "version": "1.8",
            "method": "FFT + Maxhold",
            "gps_support": False,
            "frequency_bins": np.logspace(6, 9, 1024).tolist()
        }
        """
        pass

    @abstractmethod
    def get_location(self):
        """ Get a single location point """
        pass

    @abstractmethod
    def get_spectrum(self):
        """ Get a single spectrum record """
        pass

    ############################################################################
    # OPTIONAL CALLBACKS
    ############################################################################
    def before_each_sample(self):
        """ Gets called everytime before a new sample will be acquired """
        pass

    def after_each_sample(self):
        """ Gets called everytime after a sample was acquired """
        pass

    def before_continuous_start(self):
        """ Gets called once when a continuous measurement cycle is started """
        pass

    def after_continuous_stop(self):
        """ Gets called when a continuous measurement cycle is stopped """
        pass

    def before_single_sample(self):
        """ Gets called when a single measurement is started """
        pass

    def after_single_sample(self):
        """ Gets called when a single measurement is stopped """
        pass
