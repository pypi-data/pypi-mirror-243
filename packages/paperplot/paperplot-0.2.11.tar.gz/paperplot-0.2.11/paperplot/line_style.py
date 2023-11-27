class AbstractLineStyle:
    def __init__(self):
        # control parameters
        self.color = None
        self.dashes = None
        self.label = None
        self.line_style = None
        self.line_width = None
        self.marker = None
        self.marker_edge_color = None
        self.marker_edge_width = None
        self.marker_face_color = None
        self.marker_size = None

    def decorate_line(self, line):
        if self.color is not None: line.set_color(self.color)
        if self.dashes is not None: line.set_dashes(self.dashes)
        if self.label is not None: line.set_label(self.label)
        if self.line_style is not None: line.set_linestyle(self.line_style)
        if self.line_width is not None: line.set_linewidth(self.line_width)
        if self.marker is not None: line.set_marker(self.marker)
        if self.marker_edge_color is not None: line.set_markeredgecolor(self.marker_edge_color)
        if self.marker_edge_width is not None: line.set_markeredgewidth(self.marker_edge_width)
        if self.marker_face_color is not None: line.set_markerfacecolor(self.marker_face_color)
        if self.marker_size is not None: line.set_markersize(self.marker_size)


class LineStyle:
    def __init__(self):
        pass

    @staticmethod
    def BlueCircle():
        style = AbstractLineStyle()
        style.color = (0, 0, 0, 0)
        style.marker = "o"
        style.marker_edge_color = (38/255, 148/255, 171/255, 1)

        return style

    @staticmethod
    def BrownSquare():
        style = AbstractLineStyle()
        style.color = (0, 0, 0, 0)
        style.marker = "s"
        style.marker_edge_color = (194/255, 157/255, 115/255, 1)

        return style

    @staticmethod
    def GreenDiamond():
        style = AbstractLineStyle()
        style.color = (0, 0, 0, 0)
        style.marker = "D"
        style.marker_edge_color = (126/255, 188/255, 89/255, 1)

        return style

    @staticmethod
    def GreenCircleDash():
        style = AbstractLineStyle()
        style.color = "black"
        style.line_width = 0.5
        style.line_style = (0, (8, 10))
        style.marker = "o"
        style.marker_face_color = (22/255, 119/255, 61/255, 1)
        style.marker_edge_color = (22/255, 119/255, 61/255, 1)
        style.marker_edge_width = 0.5

        return style

    @staticmethod
    def GreenStarLine():
        style = AbstractLineStyle()
        style.color = "black"
        style.line_width = 0.5
        style.marker = "*"
        style.marker_face_color = (0, 0, 0, 0)
        style.marker_edge_color = (22 / 255, 119 / 255, 61 / 255, 1)
        style.marker_edge_width = 0.5
        style.marker_size = 10

        return style

    @staticmethod
    def GreenSquareLine():
        style = AbstractLineStyle()
        style.color = "black"
        style.line_width = 0.5
        style.marker = "s"
        style.marker_face_color = (0, 0, 0, 0)
        style.marker_edge_color = (22 / 255, 119 / 255, 61 / 255, 1)
        style.marker_edge_width = 0.5

        return style

    @staticmethod
    def RedLine():
        style = AbstractLineStyle()
        style.color = (234/255, 112/255, 112/255, 1)

        return style
