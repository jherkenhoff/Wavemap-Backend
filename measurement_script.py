from abc import ABC, abstractmethod

class MeasurementScript(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_device_info(self):
        pass

    @abstractmethod
    def get_location(self):
        pass

    @abstractmethod
    def get_spectrum(self):
        pass
