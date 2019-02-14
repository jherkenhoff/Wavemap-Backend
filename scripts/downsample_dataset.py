from data_backend import Dataset
import numpy as np
import scipy.signal

original_dataset_path = "./"
original_dataset_name = "Neustadt"
original_dataset_subset = "raw"
downsampled_dataset_path = original_dataset_path
downsampled_dataset_name = original_dataset_name + "_downsampled"
downsample_factor = 100

dset_original = Dataset(original_dataset_path, original_dataset_name)
dset_downsampled = Dataset(downsampled_dataset_path, downsampled_dataset_name)

def downsample(x, n, method="mean"):
    x_padded = np.append(x, np.ones(n-len(x)%n))
    reshaped = np.reshape(x_padded, (int(len(x_padded)/n), n))
    reshaped[-1][len(x)%n:] = reshaped[-1][0:len(x)%n].mean()
    if method == "mean":
        return reshaped.mean(axis=1)
    elif method == "max":
        return reshaped.max(axis=1)
    elif method == "min":
        return reshaped.min(axis=1)

for method in ["min", "max", "mean"]:
    print("Downsampling with method \"" + method + "\"")
    dset_downsampled.create_subset(method, freq_bins=downsample(dset_original[original_dataset_subset].freq_bins[:],downsample_factor), gps_support=True)
    for i in range(dset_original[original_dataset_subset].len()):
        dset_downsampled[method].append_sample(
            time = np.datetime64("now"),
            spectrum = downsample(dset_original[original_dataset_subset].spectrum[i], downsample_factor, method=method),
            lat      = dset_original[original_dataset_subset].meta["lat"][i],
            lon      = dset_original[original_dataset_subset].meta["lon"][i],
            alt      = dset_original[original_dataset_subset].meta["alt"][i],
            speed    = dset_original[original_dataset_subset].meta["speed"][i],
            sats     = dset_original[original_dataset_subset].meta["sats"][i],
            accuracy = dset_original[original_dataset_subset].meta["accuracy"][i]
        )

dset_downsampled.close()
dset_original.close()
