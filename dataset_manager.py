from data_backend import Dataset
import os


class DatasetManager:
    def __init__(self, dataset_path):
        self.__dataset_path = dataset_path

    def get_dataset_names(self):
        names = []
        for filename in os.listdir(self.__dataset_path):
            if filename.endswith(".hdf"):
                names.append(os.path.splitext(filename)[0])
        return names
