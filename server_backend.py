from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
from data_backend import Dataset as HDF_Dataset
from dataset_manager import DatasetManager
from utils import merge_overlapping_filters

DATASET_PATH = "./datasets"
dataset_manager = DatasetManager(DATASET_PATH)
API_BASE_STR = "/api/v1"

dataset_list = []
for dset_index, name in enumerate(dataset_manager.get_dataset_names()):
    dset = HDF_Dataset(DATASET_PATH, name)
    dataset_list.append({
        "id": dset_index,
        "name": name,
        "device": {
            "name": dset.device.name,
            "version": dset.device.version
        },
        "subsets": [
            {
                "id": subset_index,
                "name": subset,
                "length": dset[subset].len(),
                "freqBins": dset[subset].freq_bins[:].tolist(),
                "link": API_BASE_STR + "/datasets/" + str(dset_index) + "/subsets/" + str(subset_index)
            } for subset_index, subset in enumerate(dset)
        ],
        "link": API_BASE_STR + "/datasets/" + str(dset_index),
    })
    dset.close()


app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("preprocessor", type=str, required=True)
parser.add_argument("filter", type=str, required=False, action="append")

class DatasetList(Resource):
    def get(self):
        return dataset_list

class Dataset(Resource):
    def get(self, dataset_id):
        return dataset_list[int(dataset_id)]

class SubsetList(Resource):
    def get(self, dataset_id):
        return dataset_list[int(dataset_id)]["subsets"]

class Subset(Resource):
    def get(self, dataset_id, subset_id):
        return dataset_list[int(dataset_id)]["subsets"][int(subset_id)]

class SampleList(Resource):
    def get(self, dataset_id, subset_id):
        dset_name = dataset_list[int(dataset_id)]["name"]
        subset_name = dataset_list[int(dataset_id)]["subsets"][int(subset_id)]["name"]
        dataset = HDF_Dataset(DATASET_PATH, dataset_list[int(dataset_id)]["name"])
        freq_bins = dataset[subset_name].attrs["freq_bins"]
        return [{
            "id": i,
            "lat": sample["lat"],
            "lon": sample["lon"],
            "spectrum": [{"freq": freq_bins[j], "mag": mag} for j, mag in enumerate(sample["spectrum"])]
        } for i, sample in enumerate(dataset[subset_name])]


class Sample(Resource):
    def get(self, dataset_id, subset_id, sample_id):
        dset_name = dataset_list[int(dataset_id)]["name"]
        subset_name = dataset_list[int(dataset_id)]["subsets"][int(subset_id)]["name"]
        dataset = HDF_Dataset(DATASET_PATH, dataset_list[int(dataset_id)]["name"])
        freq_bins = dataset[subset_name].freq_bins
        subset = dataset[subset_name]
        return {
            "id": sample_id,
            "lat": subset.meta[sample_id]["lat"],
            "lon": subset.meta[sample_id]["lon"],
            "speed": np.float64(subset.meta[sample_id]["speed"]),
            "sats": np.float64(subset.meta[sample_id]["sats"]),
            "time": int(subset.meta[sample_id]["time"]),
            "spectrum": [{"freq": freq_bins[j], "mag": mag} for j, mag in enumerate(subset.spectrum[sample_id])]
        }

class PreprocessedSampleList(Resource):
    def get(self, dataset_id, subset_id):
        dset_name = dataset_list[int(dataset_id)]["name"]
        subset_name = dataset_list[int(dataset_id)]["subsets"][int(subset_id)]["name"]
        dataset = HDF_Dataset(DATASET_PATH, dataset_list[int(dataset_id)]["name"])

        args = parser.parse_args()

        # Select preprocessor:
        if (args["preprocessor"] == "average"):
            preprocessor = lambda spectrum: spectrum.mean()
        elif (args["preprocessor"] == "max"):
            preprocessor = lambda spectrum: spectrum.max()
        elif (args["preprocessor"] == "min"):
            preprocessor = lambda spectrum: spectrum.min()
        else:
            return "Preprocessor not supported!"

        if (args["filter"] == None):
            return [{
                "id": i,
                "lat": meta["lat"],
                "lon": meta["lon"],
                "value": preprocessor(spectrum)
            } for i, (meta, spectrum) in enumerate(zip(dataset[subset_name].meta, dataset[subset_name].spectrum))]
        else:
            filters = []
            for filter in args["filter"]:
                (min, max) = filter.split(":")
                filters.append( (int(min), int(max)) )

            filters = merge_overlapping_filters(filters)

            indices = []
            for filter in filters:
                indices = np.concatenate( (indices, np.arange(filter[0], filter[1]+1)) )
            return [{
                "id": i,
                "lat": meta["lat"],
                "lon": meta["lon"],
                "value": preprocessor(spectrum)
            } for i, (meta, spectrum) in enumerate(zip(dataset[subset_name].meta, dataset[subset_name].spectrum[:,indices]))]




api.add_resource(DatasetList, API_BASE_STR +"/datasets")
api.add_resource(Dataset,     API_BASE_STR + "/datasets/<dataset_id>")
api.add_resource(SubsetList,  API_BASE_STR + "/datasets/<dataset_id>/subsets/")
api.add_resource(Subset,      API_BASE_STR + "/datasets/<dataset_id>/subsets/<subset_id>")
api.add_resource(SampleList,  API_BASE_STR + "/datasets/<dataset_id>/subsets/<subset_id>/samples")
api.add_resource(Sample,      API_BASE_STR + "/datasets/<dataset_id>/subsets/<subset_id>/samples/<int:sample_id>")
api.add_resource(PreprocessedSampleList,  API_BASE_STR + "/datasets/<dataset_id>/subsets/<subset_id>/preprocessed")

if __name__ == "__main__":
    app.run(debug=True)
