
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from dataset_manager import DatasetManager
from measurement_thread import MeasurementThread

device_setup = {
    "crazyMode": False,
    "intervalMode": "meters",
    "interval": 10
}

measurement_running = False

class LiveServer:

    def __init__(self, measurement_controller):

        self.__app = Flask(__name__)
        CORS(self.__app)

        self.__measurement_controller = measurement_controller

        # Init DatasetManager
        self.__dataset_manager = DatasetManager("./")
        self.__selected_dataset = None

        self.__socketio = SocketIO(self.__app)

        # Start measurement thread
        self.__measurement_thread = MeasurementThread(self.__socketio.emit, self.__measurement_controller)
        self.__measurement_thread.start()

        # Static server
        @self.__app.route("/")
        def hello():
            return render_template("index.html")

        # Sockets
        @self.__socketio.on("get_device_info")
        def handle_get_device_info():
            emit("update_device_info", self.__measurement_controller.get_device_info())

        @self.__socketio.on("get_datasets")
        def handle_get_datasets():
            self.__dataset_manager.scan_datasets()
            dataset_list = [{"name": dataset.name, "is_compatible": dataset.is_device_compatible(self.__measurement_controller.get_device_info())} for dataset in self.__dataset_manager.datasets]
            emit("update_datasets", dataset_list)

        @self.__socketio.on("change_measurement_running")
        def handle_change_measurement_running(value):
            measurement_running = value
            emit("update_measurement_running", measurement_running, broadcast=True)
            if value:
                self.__measurement_thread.start_continuous(3.0)
            else:
                self.__measurement_thread.stop_continuous()

        @self.__socketio.on("start_single_sample")
        def handle_start_single_sample():
            self.__measurement_thread.start_single()

        @self.__socketio.on("get_device_setup")
        def handle_get_device_setup():
            emit("update_device_setup", device_setup)

        @self.__socketio.on("select_dataset")
        def handle_select_dataset(selected):
            self.__selected_dataset = self.__dataset_manager.get_dataset_by_name(selected)
            if (self.__selected_dataset != None):
                self.__selected_dataset.get_write_access(self.__measurement_controller.get_device_info())
            dataset_name = self.__selected_dataset.name if self.__selected_dataset != None else None
            emit("update_selected_dataset", dataset_name, broadcast=True)

        @self.__socketio.on("get_selected_dataset")
        def handle_get_selected_dataset():
            dataset_name = self.__selected_dataset.name if self.__selected_dataset != None else None
            emit("update_selected_dataset", dataset_name)

        @self.__socketio.on("add_dataset")
        def handle_add_dataset(name):
            self.__selected_dataset = self.__dataset_manager.create_dataset(name, self.__measurement_controller.get_device_info())
            dataset_list = [{"name": dataset.name, "is_compatible": dataset.is_device_compatible(self.__measurement_controller.get_device_info())} for dataset in self.__dataset_manager.datasets]
            dataset_name = self.__selected_dataset.name if self.__selected_dataset != None else None
            emit("update_datasets", dataset_list, broadcast=True)
            emit("update_selected_dataset", dataset_name, broadcast=True)


    def run(self):
        """ Start the live-server"""
        self.__socketio.run(self.__app, host="0.0.0.0")
