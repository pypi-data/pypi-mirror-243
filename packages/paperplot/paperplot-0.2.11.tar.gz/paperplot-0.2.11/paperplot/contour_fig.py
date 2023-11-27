from ._figure_base import FigureBase


class ContourFig(FigureBase):
    def __init__(self):
        super().__init__()

        # control parameters
        self._color_map = "coolwarm"
        self._contour = None
        self._level_num = 900

    def set_color_map(self, color_map):
        self._color_map = color_map

    def set_data(self, X, Y, Z, ):
        self._contour = self._axes.contourf(X, Y, Z, self._level_num, cmap=self._color_map)

    def set_level_num(self, num):
        self._level_num = num

