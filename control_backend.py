from abc import ABC, abstractmethod
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

device_setup = {
    "crazyMode": False,
    "intervalMode": "meters",
    "interval": 10
}

datasets = [
]

selected_dataset = None

measurement_running = False


class ControlBackend(ABC):
    app = None
    socketio = None

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "secret!"
        self.app.config['DEBUG'] = True
        CORS(self.app)

        self.socketio = SocketIO(self.app)

        # Static server
        @self.app.route("/")
        def hello():
            return render_template("index.html")

        # Sockets
        @self.socketio.on("get_device_info")
        def handle_get_device_info():
            emit("update_device_info", self.get_device_info())

        @self.socketio.on("get_datasets")
        def handle_get_datasets():
            emit("update_datasets", datasets)

        @self.socketio.on("change_measurement_running")
        def handle_start_measurement(value):
            measurement_running = value
            emit("update_measurement_running", measurement_running, broadcast=True)

        @self.socketio.on("get_device_setup")
        def handle_get_device_setup():
            emit("update_device_setup", device_setup)

        @self.socketio.on("select_dataset")
        def handle_select_dataset(selected):
            global selected_dataset
            selected_dataset = selected
            emit("update_selected_dataset", selected_dataset, broadcast=True)

        @self.socketio.on("get_selected_dataset")
        def handle_get_selected_dataset():
            global selected_dataset
            emit("update_selected_dataset", selected_dataset)

        @self.socketio.on("add_dataset")
        def handle_add_dataset(name):
            global selected_dataset
            if (len(datasets) == 0):
                id = 0
            else:
                id = datasets[-1]["id"] + 1
            datasets.append({"id": id, "name": name, "points": 0})
            selected_dataset = id
            emit("update_datasets", datasets, broadcast=True)
            emit("update_selected_dataset", selected_dataset, broadcast=True)

    def run(self):
        self.socketio.run(self.app, host="0.0.0.0")

    @abstractmethod
    def get_device_info():
        pass



if __name__ == "__main__":
    control_backend = ControlBackend()
