from ._figure_base import FigureBase
from .line_style import AbstractLineStyle


class LineFig(FigureBase):
    def __init__(self):
        super().__init__()

        # initialize
        self._axes.minorticks_on()

    def add_background_grid(self):
        self._axes.grid(color=(235/255, 235/255, 235/255))

    def add_line(self, x, y, style, label=None):
        # check
        if not isinstance(style, AbstractLineStyle):
            raise TypeError("The input style is not a type of 'LineStyle'.")

        # add
        line, = self._axes.plot(x, y)
        style.decorate_line(line)

        if label is not None: line.set_label(label)
