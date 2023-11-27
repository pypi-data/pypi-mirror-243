from ._figure_base import FigureBase
import matplotlib.tri as tri


class MeshFig(FigureBase):
    def __init__(self):
        super().__init__()

    def set_data(self, cells, nodes):
        triangle = tri.Triangulation(nodes[:, 0], nodes[:, 1], cells)
        self._axes.triplot(triangle, "k-", lw=0.7)
