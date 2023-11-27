import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from ._figure_base import FigureBase


class PixelContourFig(FigureBase):
    def __init__(self):
        super().__init__()

        # control parameters
        self._color_axes = None
        self._color_bar = None
        self._pixel_contour = None

    def remove_color_axes_outline(self):
        self._color_bar.outline.set_edgecolor("none")

    def set_grid_data(self, X, Y, Z, color_bar=True):
        # pixel contour
        self._pixel_contour = self._axes.pcolormesh(X, Y, Z, shading="flat", cmap="viridis")

        # color bar
        if color_bar: self._add_color_axes()

    def set_triangles_data(self, nodes, cells, scalars, color_bar=True, clim=None):
        # create scalar mappable
        v_min = 0
        v_max = 0
        if clim is None:
            v_min = np.min(scalars)
            v_max = np.max(scalars)
        else:
            v_min = clim[0]
            v_max = clim[1]
        self._pixel_contour = cm.ScalarMappable(cmap=plt.cm.viridis, norm=mcolors.Normalize(v_min, v_max))

        # pixel contour
        for i, triangle in enumerate(cells):
            t_coords = np.array([[nodes[triangle[0]][0], nodes[triangle[0]][1]],
                                 [nodes[triangle[1]][0], nodes[triangle[1]][1]],
                                 [nodes[triangle[2]][0], nodes[triangle[2]][1]]])

            triangle_patch = patches.Polygon(t_coords, color=plt.cm.viridis((scalars[i]-v_min)/(v_max-v_min)))
            self._axes.add_patch(triangle_patch)

        # color bar
        if color_bar: self._add_color_axes()

        # default settings
        self.set_x_axis(lim=(np.min(nodes[:, 0]), np.max(nodes[:, 0])))
        self.set_y_axis(lim=(np.min(nodes[:, 1]), np.max(nodes[:, 1])))

    def set_color_axes(self, title=None, lim=None, ticks=None):
        if title is not None:
            self._color_bar.ax.set_title(title, loc="center")

        if lim is not None:
            self._color_bar.ax.set_ylim(lim)
            self._pixel_contour.set_clim(lim)

        if ticks is not None:
            self._color_bar.set_ticks(ticks)

    def _add_color_axes(self):
        axes_pos = self._axes.get_position()
        self._color_axes = self._fig.add_axes([axes_pos.x1 + 0.02, axes_pos.y0, 0.02, axes_pos.height])
        self._color_bar = self._fig.colorbar(self._pixel_contour, cax=self._color_axes, orientation='vertical')
