from dataset import Dataset
import os
import re

class DatasetManager:

    file_extension = ".hdf"

    def __init__(self, base_path):
        self.__base_path = base_path
        self.datasets = []
        self.scan_datasets()

    def scan_datasets(self):
        self.datasets = [Dataset(f) for f in os.listdir(self.__base_path) if re.match(r".*\%s" %DatasetManager.file_extension, f)]

    def create_dataset(self, name, device_info):
        """Create a new dataset if the name is not already occupied by an existing dataset"""
        path = os.path.join(self.__base_path, name + DatasetManager.file_extension)
        if os.path.isfile(path):
            raise Exception("Dataset '%s' is already existing (%s)" %(name, path))

        dataset = Dataset(path, device_info)
        self.datasets.append(dataset)
        return dataset

    def get_compatible_datasets(self, device_info):
        return [dataset for dataset in self.datasets if dataset.is_device_compatible(device_info)]


    def get_dataset_by_name(self, name):
        for dataset in self.datasets:
            if (dataset.name == name):
                return dataset

        return None


if __name__ == '__main__':
    manager = DatasetManager("/home/jost/Projects/Controller-Backend/");
