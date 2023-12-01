#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Matplotlib imports
from matplotlib.backends.backend_pdf import PdfPages

# Other imports
import numpy
from dataclasses import dataclass
from MPSPlots.render2D.artist import (
    Line,
    FillLine,
    STDLine,
    Mesh,
    Scatter,
    Contour,
    VerticalLine,
    HorizontalLine,
    Text,
    PatchPolygon,
    Colorbar,
    AxAnnotation,
    Table,
    WaterMark
)


@dataclass
class Axis:
    row: int
    """ Row value of the ax """
    col: int
    """ Column value of the ax """
    x_label: str = None
    """ Set x label """
    y_label: str = None
    """ Set y label """
    title: str = ''
    """ Title of the ax """
    show_grid: bool = True
    """ Show the ax grid or not """
    show_legend: bool = False
    """ Show the legend or not """
    x_scale: str = 'linear'
    """ Set scale of x axis """
    y_scale: str = 'linear'
    """ Set scale of y axis """
    x_limits: list = None
    """ Set limits of x axis """
    y_limits: list = None
    """ Set limits of y axis """
    equal_limits: bool = False
    """ Set equal limits to x and y axis, override x_limits and y_limits """
    equal: bool = False
    """ Set aspect ratio to equal """
    water_mark: str = ''
    """ Watermark to add to axis """
    projection: str = None
    """ Projection of the plot [Polar, normal] """
    font_size: int = 16
    """ Text font size """
    tick_size: int = 14
    """ Ticks font size """
    y_tick_position: str = 'left'
    """ Ticks position for the y axis, must be in ['left', 'right'] """
    x_tick_position: str = 'left'
    """ Ticks position for the x axis, must be in ['top', 'bottom'] """
    show_ticks: bool = True
    """ Show x and y ticks or not """
    show_colorbar: bool = None
    """ Show colorbar or not """
    legend_font_size: bool = 14
    """  Font size of the legend text """
    line_width: float = None
    """ Line width of the contained artists. """
    line_style: float = None
    """ Line style of the contained artists. """
    x_scale_factor: float = None
    """ Scaling factor for the x axis """
    y_scale_factor: float = None
    """ Scaling factor for the y axis """

    def __post_init__(self):
        self._artist_list = []
        self.mpl_ax = None
        self.colorbar = Colorbar()

    def __getitem__(self, idx):
        return self._artist_list[idx]

    def __add__(self, other):
        self._artist_list += other._artist_list
        return self

    def add_artist_to_ax(function):
        def wrapper(self, *args, **kwargs):
            artist = function(self, *args, **kwargs)
            self._artist_list.append(artist)

            return artist

        return wrapper

    @property
    def style(self):
        return {
            'x_label': self.x_label,
            'y_label': self.y_label,
            'title': self.title,
            'show_grid': self.show_grid,
            'show_legend': self.show_legend,
            'x_scale': self.x_scale,
            'y_scale': self.y_scale,
            'x_limits': self.x_limits,
            'y_limits': self.y_limits,
            'equal_limits': self.equal_limits,
            'equal': self.equal,
            'colorbar': self.colorbar,
            'water_mark': self.water_mark,
            'projection': self.projection,
            'font_size': self.font_size,
            'legend_font_size': self.legend_font_size,
            'tick_size': self.tick_size
        }

    def get_y_max(self) -> float:
        """
        Gets the maximum y value of all artist in that current axis

        :returns:   The maximum y value.
        :rtype:     float
        """
        y_max = -numpy.inf
        for artist in self._artist_list:
            if not hasattr(artist, 'y'):
                continue
            artist_y_max = numpy.max(artist.y)
            y_max = max(y_max, artist_y_max)

        return y_max

    def get_y_min(self) -> float:
        """
        Gets the minimum y value of all artist in that current axis

        :returns:   The minimum y value.
        :rtype:     float
        """
        y_min = numpy.inf
        for artist in self._artist_list:
            if not hasattr(artist, 'y'):
                continue
            artist_y_min = numpy.min(artist.y)
            y_min = min(y_min, artist_y_min)

        return y_min

    def get_x_max(self) -> float:
        """
        Gets the maximum x value of all artist in that current axis

        :returns:   The maximum x value.
        :rtype:     float
        """
        y_max = -numpy.inf
        for artist in self._artist_list:
            artist_y_max = numpy.max(artist.y)
            y_max = max(y_max, artist_y_max)

        return y_max

    def get_x_min(self) -> float:
        """
        Gets the minimum y value of all artist in that current axis

        :returns:   The minimum y value.
        :rtype:     float
        """
        x_min = numpy.inf
        for artist in self._artist_list:
            artist_x_min = numpy.min(artist.y)
            x_min = min(x_min, artist_x_min)

        return x_min

    def copy_style(self, other) -> None:
        assert isinstance(other, self), f"Cannot copy style from other class {other.__class__}"
        for element, value in other.style.items():
            setattr(self, element, value)

    def add_artist(self, *artists) -> None:
        for artist in artists:
            self._artist_list.append(artist)

    def set_style(self, **style_dict):
        for element, value in style_dict.items():
            setattr(self, element, value)

        return self

    def set_ax_limits(self) -> None:
        """
        Sets the ax x and y limits.

        :returns:   No returns
        :rtype:     None
        """
        self.mpl_ax.set_xlim(self.x_limits)

        self.mpl_ax.set_ylim(self.y_limits)

        if self.equal_limits:
            xy_limits = [*self.mpl_ax.get_xlim(), *self.mpl_ax.get_ylim()]
            min_xy_limit = numpy.min(xy_limits)
            max_xy_limit = numpy.max(xy_limits)

            self.mpl_ax.set_xlim([min_xy_limit, max_xy_limit])
            self.mpl_ax.set_ylim([min_xy_limit, max_xy_limit])

    def _render_(self) -> None:
        """
        Renders the ax with each of its related artist.

        :returns:   No returns
        :rtype:     None
        """
        for artist in self._artist_list:
            if self.x_scale_factor is not None:
                artist.x_scale_factor = self.x_scale_factor

            if self.y_scale_factor is not None:
                artist.y_scale_factor = self.y_scale_factor

            if self.line_width is not None:
                artist.line_width = self.line_width

            if self.line_style is not None:
                artist.line_style = self.line_style

            artist._render_(self)

        self._decorate_ax_()

        if self.show_colorbar:
            self.colorbar._render_(ax=self)

        self.set_ax_limits()

    def generate_legend(self) -> None:
        """
        Generate legend of ax

        :returns:   No returns
        :rtype:     None
        """
        if self.show_legend:
            self.mpl_ax.legend()
            handles, labels = self.mpl_ax.get_legend_handles_labels()

            by_label = dict(zip(labels, handles))

            self.mpl_ax.legend(
                by_label.values(),
                by_label.keys(),
                edgecolor='k',
                facecolor='white',
                fancybox=True,
                fontsize=self.legend_font_size - 4
            )

    def _decorate_ax_(self):
        self.generate_legend()

        if self.x_label is not None:
            self.mpl_ax.set_xlabel(self.x_label, fontsize=self.font_size)

        if self.y_label is not None:
            self.mpl_ax.set_ylabel(self.y_label, fontsize=self.font_size)

        if self.x_tick_position.lower() == 'top':
            self.mpl_ax.xaxis.tick_top()
            self.mpl_ax.xaxis.set_label_position("top")

        elif self.x_tick_position.lower() == 'bottom':
            self.mpl_ax.xaxis.tick_bottom()
            self.mpl_ax.xaxis.set_label_position("bottom")

        if self.y_tick_position.lower() == 'right':
            self.mpl_ax.yaxis.tick_right()
            self.mpl_ax.yaxis.set_label_position("right")

        elif self.y_tick_position.lower() == 'left':
            self.mpl_ax.yaxis.tick_left()
            self.mpl_ax.yaxis.set_label_position("left")

        if self.title is not None:
            self.mpl_ax.set_title(self.title, fontsize=self.font_size)

        if self.x_scale is not None:
            self.mpl_ax.set_xscale(self.x_scale)

        if self.y_scale is not None:
            self.mpl_ax.set_yscale(self.y_scale)

        if self.tick_size is not None:
            self.mpl_ax.tick_params(labelsize=self.tick_size)

        if self.equal:
            self.mpl_ax.set_aspect("equal")

        if self.show_grid:
            self.mpl_ax.grid(self.show_grid)

        self.mpl_ax.axes.get_xaxis().set_visible(self.show_ticks)
        self.mpl_ax.axes.get_yaxis().set_visible(self.show_ticks)

        self.add_watermark(text=self.water_mark)

    @add_artist_to_ax
    def add_fill_line(self, **kwargs: dict) -> FillLine:
        """
        Adds a FillLine artist to ax.

        :param      kwargs:  The keywords arguments to be sent to FillLine class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     FillLine
        """
        return FillLine(**kwargs)

    @add_artist_to_ax
    def add_std_line(self, **kwargs: dict) -> STDLine:
        """
        Adds a STDLine artist to ax.

        :param      kwargs:  The keywords arguments to be sent to STDLine class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     STDLine
        """
        return STDLine(**kwargs)

    @add_artist_to_ax
    def add_scatter(self, **kwargs: dict) -> Scatter:
        """
        Adds a Scatter artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Scatter class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Scatter
        """
        return Scatter(**kwargs)

    def add_table(self, **kwargs: dict) -> Table:
        """
        Adds a Table artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Table class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Table
        """
        return Table(**kwargs)

    @add_artist_to_ax
    def add_mesh(self, **kwargs: dict) -> Mesh:
        """
        Adds a Mesh artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Mesh class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Mesh
        """
        artist = Mesh(**kwargs)
        self.add_artist(artist)

        return artist

    @add_artist_to_ax
    def add_contour(self, **kwargs: dict) -> Contour:
        """
        Adds a Contour artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Contour class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Contour
        """
        return Contour(**kwargs)

    @add_artist_to_ax
    def add_line(self, **kwargs: dict) -> Line:
        """
        Adds a Line artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Line class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Line
        """
        return Line(**kwargs)

    @add_artist_to_ax
    def add_vertical_line(self, **kwargs: dict) -> VerticalLine:
        """
        Adds a VerticalLine artist to ax.

        :param      kwargs:  The keywords arguments to be sent to VerticalLine class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     VerticalLine
        """
        return VerticalLine(**kwargs)

    @add_artist_to_ax
    def add_horizontal_line(self, **kwargs: dict) -> HorizontalLine:
        """
        Adds a HorizontalLine artist to ax.

        :param      kwargs:  The keywords arguments to be sent to HorizontalLine class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     VerticalLine
        """
        return HorizontalLine(**kwargs)

    @add_artist_to_ax
    def add_text(self, **kwargs: dict) -> Text:
        """
        Adds a Text artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Text class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Text
        """
        return Text(**kwargs)

    @add_artist_to_ax
    def add_watermark(self, **kwargs: dict) -> WaterMark:
        """
        Adds a WaterMark artist to ax.

        :param      kwargs:  The keywords arguments to be sent to WaterMark class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Text
        """
        return WaterMark(**kwargs)

    @add_artist_to_ax
    def add_polygon(self, **kwargs: dict) -> Text:
        """
        Adds a Text artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Text class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Text
        """
        return PatchPolygon(**kwargs)

    def add_colorbar(self, **kwargs: dict) -> Colorbar:
        """
        Adds a Colorbar artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Colorbar class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Colorbar
        """
        self.colorbar = Colorbar(**kwargs)
        self.show_colorbar = True

        return self.colorbar

    @add_artist_to_ax
    def add_ax_annotation(self, text: str, **kwargs: dict) -> Colorbar:
        """
        Adds a Colorbar artist to ax.

        :param      kwargs:  The keywords arguments to be sent to Colorbar class
        :type       kwargs:  dict

        :returns:   The artist object
        :rtype:     Colorbar
        """
        return AxAnnotation(text, **kwargs)


def Multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)

    for fig in figs:
        fig._mpl_figure.savefig(pp, format='pdf')

    pp.close()


# -
