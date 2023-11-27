import numpy as np


class DataFilterBase:
    def __init__(self):
        self._data = None

    def get_data(self):
        return self._data

    def read_data_from_csv(self, filename):
        self._data = np.loadtxt(filename, dtype=np.double, delimiter=",")

    def set_data(self, data):
        self._data = data
