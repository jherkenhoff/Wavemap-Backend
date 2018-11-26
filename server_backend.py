from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from data_backend import Dataset as HDF_Dataset
from dataset_manager import DatasetManager

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
                "link": API_BASE_STR + "/datasets/" + str(dset_index) + "/subsets/" + str(subset_index)
            } for subset_index, subset in enumerate(dset)
        ],
        "link": API_BASE_STR + "/datasets/" + str(dset_index),
    })
    dset.close()

print(dataset_list)

app = Flask(__name__)
CORS(app)
api = Api(app)

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
        return "Noch nicht implementiert"

class PreprocessedSampleList(Resource):
    def get(self, dataset_id, subset_id):
        dset_name = dataset_list[int(dataset_id)]["name"]
        subset_name = dataset_list[int(dataset_id)]["subsets"][int(subset_id)]["name"]
        dataset = HDF_Dataset(DATASET_PATH, dataset_list[int(dataset_id)]["name"])

        return [{
            "id": i,
            "lat": sample["lat"],
            "lon": sample["lon"]
        } for i, sample in enumerate(dataset[subset_name])]

api.add_resource(DatasetList, API_BASE_STR +"/datasets")
api.add_resource(Dataset,     API_BASE_STR + "/datasets/<dataset_id>")
api.add_resource(SubsetList,  API_BASE_STR + "/datasets/<dataset_id>/subsets/")
api.add_resource(Subset,      API_BASE_STR + "/datasets/<dataset_id>/subsets/<subset_id>")
api.add_resource(SampleList,  API_BASE_STR + "/datasets/<dataset_id>/subsets/<subset_id>/samples")
api.add_resource(PreprocessedSampleList,  API_BASE_STR + "/datasets/<dataset_id>/subsets/<subset_id>/preprocessed")

if __name__ == "__main__":
    app.run(debug=True)
