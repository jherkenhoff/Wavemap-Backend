import os
import matplotlib.pyplot as plt

class Thumbnailer:
    def __init__(self, thumbnail_folder):
        self.__thumbnail_folder = thumbnail_folder

    def clean(self):
        pass

    def create_thumbnail(self, dataset_id, subset_id, subset):

        lat = [sample["lat"] for sample in subset.meta]
        lon = [sample["lon"] for sample in subset.meta]

        fig = plt.figure()
        ax = plt.Axes(fig, [0., 0., 1., 1.], )
        ax.set_aspect('equal')
        ax.set_axis_off()
        fig.add_axes(ax)
        plt.plot(lon, lat, color='#ee6a35', lw=2, alpha=0.8)
        fig.savefig(self.get_thumbnail_path(dataset_id, subset_id), transparent=True)

    def get_thumbnail_path(self, dataset_id, subset_id):
        return os.path.join(self.__thumbnail_folder, "dataset"+str(dataset_id) + "_subset"+str(subset_id) + ".png")
