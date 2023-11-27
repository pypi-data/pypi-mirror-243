import numpy as np
from ._data_filter_base import DataFilterBase


class MeshGridFilter(DataFilterBase):
    def __init__(self):
        super().__init__()

        self._x_interval = None
        self._x_params = None
        self._y_interval = None
        self._y_params = None

    def filter(self):
        x = np.linspace(self._x_params[0], self._x_params[1], self._x_params[2], endpoint=True)
        y = np.linspace(self._y_params[0], self._y_params[1], self._y_params[2], endpoint=True)

        X, Y = np.meshgrid(x, y)
        Z = np.zeros([x.size - 1, y.size - 1])

        for i in range(self.__data_cell_num()):
            if self.__is_in_chosen_area(self._data[i]):
                x_idx = self.__calc_x_idx(self._data[i][0])
                y_idx = self.__calc_y_idx(self._data[i][1])
                Z[y_idx][x_idx] = self._data[i][3]

        return X, Y, Z

    def set_x_params(self, params):
        self._x_params = params
        self._x_interval = (self._x_params[1] - self._x_params[0]) / (self._x_params[2] - 1)

    def set_y_params(self, params):
        self._y_params = params
        self._y_interval = (self._y_params[1] - self._y_params[0]) / (self._y_params[2] - 1)

    def __calc_x_idx(self, coordinate):
        return int((coordinate - self._x_params[0])//self._x_interval)

    def __calc_y_idx(self, coordinate):
        return int((coordinate - self._y_params[0])//self._y_interval)

    def __data_cell_num(self):
        return self._data.shape[0]

    def __is_in_chosen_area(self, params):
        if params[0]>self._x_params[0] and params[0]<self._x_params[1] and \
           params[1]>self._y_params[0] and params[1]<self._y_params[1]:
            return True
        else:
            return False
