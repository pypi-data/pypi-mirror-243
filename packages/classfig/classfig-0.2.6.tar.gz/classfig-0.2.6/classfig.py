#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" classfig simplifies figure handling with matplotlib:

- predefinied templates
- figure instantiation in a class object
- simplified handling (e.g. plot with vectors)

from classfig import classfig
# very simple example
fig = classfig()
fig.plot()
fig.show()

# more complex example
fig = classfig("l", nrows=2, sharex=True)  # create figure with template l=large
fig.plot([1, 2, 3, 1, 2, 3, 4, 1, 1])  # plot first data set
fig.title("First data set")  # set title for subplot
fig.subplot()  # set focus to next subplot/axis
fig.plot([0, 1, 2, 3, 4], [0, 1, 1, 2, 3], label="random")  # plot second data set
fig.legend()  # generate legend
fig.grid()  # show translucent grid to highlight major ticks
fig.xlabel("Data")  # create xlabel for second axis
fig.save("fig1.png", "pdf")  # save figure to png and pdf

# The handlers fig.figH, fig.plotH, fig.axeH and fig.axeC can be used for
# to access all matplotlib functionality.
fig.axeC.

"""
# %%
__author__ = "Fabian Stutzki"
__email__ = "fast@fast-apps.de"
__version__ = "0.2.6"

import pathlib
import os
import json
import numpy as np
from packaging import version
import matplotlib
import matplotlib.pyplot
from cycler import cycler


# %%
class classfig:
    """
    classfig simplifies figure handling with matplotlib

    Use as
    from classfig import classfig
    fig = classfig('m')
    fig.plot([0,1,2,3,4],[0,1,1,2,3])
    fig.save('test.png')

    @author: fstutzki

    """

    def __init__(
        self,
        *args,
        template="m",
        nrows=1,
        ncols=1,
        isubplot=0,
        sharex=False,
        sharey=False,
        width=None,
        height=None,
        fontfamily=None,
        fontsize=None,
        linewidth=None,
        show=True,
        vspace=None,
        hspace=None,
        presets=None,
    ):
        """Set default values and create figure: fig = classfig('OL',(2,2))"""

        # Assign unnamed arguments
        if len(args) == 1:
            if isinstance(args[0], int):
                nrows = args[0]
            else:
                template = args[0]
        elif len(args) == 2:
            if isinstance(args[0], int):
                nrows = args[0]
                ncols = args[1]
            else:
                template = args[0]
                nrows = args[1]
        elif len(args) == 3:
            template = args[0]
            nrows = args[1]
            ncols = args[2]
        elif len(args) > 3:
            raise ValueError(
                "Too many arguments! classfig() accepts a maximum of 3 arguments."
            )

        # Initialize presets dictionary
        self.presets = dict()

        # Load default presets from json
        if os.path.isfile("classfig_presets.json"):
            self.load_presets("classfig_presets.json")

        if isinstance(presets, str) and os.path.isfile(presets):
            # presets are given as json file path
            self.load_presets(presets)
        elif isinstance(presets, dict):
            # presets are given as dictionary
            self.presets.update(presets)

        # Add internal presets
        if "m" not in self.presets.keys():
            self.presets["m"] = {
                "width": 15,
                "height": 10,
                "fontfamily": "sans-serif",
                "fontsize": 12,
                "linewidth": 2,
            }
        if "s" not in self.presets.keys():
            self.presets["s"] = {
                "width": 10,
                "height": 8,
                "fontfamily": "sans-serif",
                "fontsize": 12,
                "linewidth": 2,
            }
        if "l" not in self.presets.keys():
            self.presets["l"] = {
                "width": 20,
                "height": 15,
                "fontfamily": "sans-serif",
                "fontsize": 12,
                "linewidth": 3,
            }
        if "ol" not in self.presets.keys():
            self.presets["ol"] = {
                "width": 8,
                "height": 6,
                "fontfamily": "serif",
                "fontsize": 9,
                "linewidth": 1,
            }
        if "oe" not in self.presets.keys():
            self.presets["oe"] = {
                "width": 12,
                "height": 8,
                "fontfamily": "serif",
                "fontsize": 10,
                "linewidth": 1,
            }
        if "square" not in self.presets.keys():
            self.presets["square"] = {
                "width": 10,
                "height": 10,
                "fontfamily": "serif",
                "fontsize": 10,
                "linewidth": 1,
            }
        if "colors" not in self.presets.keys():
            self.presets["colors"] = {
                "blue": (np.array([33, 101, 146]) / 255),
                "red": (np.array([218, 4, 19]) / 255),
                "green": (np.array([70, 173, 52]) / 255),
                "orange": (np.array([235, 149, 0]) / 255),
                "yellow": (np.array([255, 242, 0]) / 255),
                "grey": (np.array([64, 64, 64]) / 255),
            }
        if "color_seq" not in self.presets.keys():
            self.presets["color_seq"] = ["blue", "red", "green", "orange"]
        if "linestyle_seq" not in self.presets.keys():
            self.presets["linestyle_seq"] = ["-", "--", ":", "-."]

        # rename old templates, maybe removed in upcoming version
        template = template.lower()
        if template == "ppt":
            template = "m"
        if template == "ppttwo":
            template = "s"
        if template == "pptbig":
            template = "l"

        # check if template exists (ignoring case), otherwise set template m (default)
        if template not in self.presets:
            template = "m"

        # for key, value in templates[template].items():
        if width is None:
            if "width" in self.presets[template]:
                width = self.presets[template]["width"]
            else:
                width = self.presets["m"]["width"]
        if height is None:
            if "height" in self.presets[template]:
                height = self.presets[template]["height"]
            else:
                height = self.presets["m"]["height"]
        if fontfamily is None:
            if "fontfamily" in self.presets[template]:
                fontfamily = self.presets[template]["fontfamily"]
            else:
                fontfamily = self.presets["m"]["fontfamily"]
        if fontsize is None:
            if "fontsize" in self.presets[template]:
                fontsize = self.presets[template]["fontsize"]
            else:
                fontsize = self.presets["m"]["fontsize"]
        if linewidth is None:
            if "linewidth" in self.presets[template]:
                linewidth = self.presets[template]["linewidth"]
            else:
                linewidth = self.presets["m"]["linewidth"]

        # define colors from presets
        self.colors = dict()
        for iname, icolor in self.presets["colors"].items():
            if np.max(icolor) > 1:
                self.colors[iname] = np.array(icolor) / 255
            else:
                self.colors[iname] = np.array(icolor)

        # apply parameters to matplotlib
        matplotlib.rc("font", size=fontsize)
        matplotlib.rc("font", family=fontfamily)
        matplotlib.rc("lines", linewidth=linewidth)
        self.set_cycle()

        # store global variables
        self.figshow = show  # show figure after saving
        self.axe_current = 0
        self.barH = None
        self.plotH = None
        self.surfaceH = None
        self.linewidth = linewidth

        # Create figure
        self.figH = matplotlib.pyplot.figure()
        self.figH.set_size_inches(width / 2.54, height / 2.54)
        self.subplot(
            nrows,
            ncols,
            isubplot,
            sharex=sharex,
            sharey=sharey,
            vspace=vspace,
            hspace=hspace,
        )

    #        if template.lower() == 'square':
    #            self.axeC.margins(0)
    #            self.axeC.axis('off')
    #            self.axeC.set_position([0, 0, 1, 1])

    def subplot(
        self,
        *args,
        nrows=None,
        ncols=None,
        index=None,
        sharex=False,
        sharey=False,
        vspace=None,
        hspace=None,
    ):
        """
        Set current axis/subplot: fig.subplot(0) for first subplot
        or fig.subplot() for next subplot
        """

        num_args = len(args)
        if num_args == 0:
            # increase current axe handle by 1
            self.axe_current += 1
        elif num_args == 1:
            # define current axe handle
            self.axe_current = args[0]
        elif num_args == 2 or num_args == 3:
            # generate new subplot
            nrows = args[0]
            ncols = args[1]
        else:
            raise ValueError("classfig.subplot() takes 0 to 3 unnamed arguments")

        if nrows is not None or ncols is not None:
            # generate new subplot
            if nrows is None:
                nrows = 1
            if ncols is None:
                ncols = 1
            self.subplot_nrows = nrows
            self.subplot_ncols = ncols
            self.subplot_sharex = sharex
            self.subplot_sharey = sharey
            self.subplot_vspace = vspace
            self.subplot_hspace = hspace
            if num_args == 3:
                self.axe_current = args[2]
            else:
                self.axe_current = 0
            try:
                self.figH.clf()
                self.figH, self.axeH = matplotlib.pyplot.subplots(
                    nrows=self.subplot_nrows,
                    ncols=self.subplot_ncols,
                    num=self.figH.number,
                    sharex=self.subplot_sharex,
                    sharey=self.subplot_sharey,
                )
            except Exception as excpt:
                print("classfig.subplot(): Matplotlib cannot generate subplots.")
                print(excpt)

        # overwrite axe_current with named argument
        if index is not None:
            self.axe_current = index

        # set current axe handle
        self.axe_current = self.axe_current % (self.subplot_nrows * self.subplot_ncols)
        if self.subplot_nrows == 1 and self.subplot_ncols == 1:
            self.axeC = self.axeH
        elif self.subplot_nrows > 1 and self.subplot_ncols > 1:
            isuby = self.axe_current // self.subplot_ncols
            isubx = self.axe_current % self.subplot_ncols
            self.axeC = self.axeH[isuby][isubx]
        else:
            self.axeC = self.axeH[self.axe_current]

    #        if np.size(self.figH.get_axes()) <= self.axe_current:
    # self.axeC = matplotlib.pyplot.subplot(
    #     self.subplot_nrows, self.subplot_ncols, self.axe_current
    # )  # ,True,False)

    #        else:
    #        print(self.figH.get_axes())
    #        self.axeC = self.figH.get_axes()[self.axe_current-1]
    #        return self.axeC

    def load_presets(self, filepath):
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
            self.presets.update(data)
        except FileNotFoundError:
            print(f"File not found: '{filepath}'")
        except IOError as e:
            print(f"IOError when reading '{filepath}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{filepath}': {e}")

    def generate_preset_example(self, filepath="classfig_presets_example.json"):
        """generates a preset example that can be modified for custom presets

        Args:
            filepath (str, optional): Path to JSON file. Defaults to "classfig_presets_example.json".
        """
        example_dict = dict()
        example_dict["m"] = self.presets["m"]
        example_dict["s"] = self.presets["s"]
        example_dict["l"] = self.presets["l"]
        example_dict["colors"] = self.presets["colors"]
        example_dict["color_seq"] = self.presets["color_seq"]
        example_dict["linestyle_seq"] = self.presets["linestyle_seq"]

        for icolor in example_dict["colors"]:
            example_dict["colors"][icolor] = tuple(example_dict["colors"][icolor] * 255)

        # write example_dict to JSON file
        with open(filepath, "w") as file:
            json.dump(example_dict, file)

    def suptitle(self, *args, **kwargs):
        """Set super title for the whole figure"""
        self.figH.suptitle(*args, **kwargs)

    def bar(self, *args, **kwargs):
        """Generate bar plot"""
        self.barH = self.axeC.bar(*args, **kwargs)
        return self.barH

    def plot(
        self,
        mat=np.array(
            [[1, 2, 3, 4, 5, 6, 7], np.random.randn(7), 2 * np.random.randn(7)]
        ),
        *args,
        **kwargs,
    ):
        """plot() generates a line plot"""
        if np.ndim(mat) > 1:
            if np.shape(mat)[0] > np.shape(mat)[1]:
                mat = mat.T
            for imat in mat[1:]:
                self.plotH = self.axeC.plot(mat[0, :], imat, *args, **kwargs)
            return self.plotH
        else:
            self.plotH = self.axeC.plot(mat, *args, **kwargs)
            return self.plotH

    # def plot(
    #     self,
    #     *args,
    #     **kwargs,
    # ):
    #     """Generate line plot"""
    #     if args:
    #         # if np.ndim(args[0]) > 1:
    #         #     if np.shape(args[0])[0] > np.shape(args[0])[1]:
    #         #         args[0] = args[0].T
    #         #     for irow in args[0][1:]:
    #         #         print("Plot")
    #         #         print(args[0][0,:])
    #         #         print(irow)
    #         #         self.plotH = self.axeC.plot(args[0][0, :], irow, **kwargs)
    #         #     return self.plotH
    #         # else:
    #         print(args)
    #         self.plotH = self.axeC.plot(*args, **kwargs)
    #         return self.plotH
    #     else:
    #         self.plot(np.array(
    #             [[1, 2, 3, 4, 5, 6, 7, 8], np.random.randn(8), 2 * np.random.randn(8)]
    #         ),**kwargs)

    def semilogx(self, *args, **kwargs):
        """Semi-log plot on x axis"""
        self.plot(*args, **kwargs)
        self.xscale("log")

    def semilogy(self, *args, **kwargs):
        """Semi-log plot on y axis"""
        self.plot(*args, **kwargs)
        self.yscale("log")

    def fill_between(self, *args, color=None, alpha=0.1, linewidth=0, **kwargs):
        """fill area below / between lines"""
        if color is None:
            color = self.colorLast()
        self.axeC.fill_between(
            *args, color=color, alpha=alpha, linewidth=linewidth, **kwargs
        )

    def colorLast(self):
        """returns the last color code used by plot"""
        return self.plotH[0].get_color()

    def pcolor(self, *args, **kwargs):
        """2D area plot"""
        if "cmap" not in kwargs:
            kwargs["cmap"] = "nipy_spectral"
        self.surfaceH = self.axeC.pcolormesh(*args, **kwargs)
        return self.surfaceH

    def pcolor_log(self, *args, vmin=False, vmax=False, **kwargs):
        """2D area plot with logarithmic scale"""
        if "cmap" not in kwargs:
            kwargs["cmap"] = "nipy_spectral"
        kwargs_log = dict()
        if vmin is not False:
            kwargs_log["vmin"] = vmin
        if vmax is not False:
            kwargs_log["vmax"] = vmax
        kwargs["norm"] = matplotlib.colors.LogNorm(**kwargs_log)
        self.surfaceH = self.axeC.pcolormesh(*args, **kwargs)
        return self.surfaceH

    def pcolor_square(self, *args, **kwargs):
        """2D area plot with axis equal and off"""
        if "cmap" not in kwargs:
            kwargs["cmap"] = "nipy_spectral"
        self.surfaceH = self.axeC.pcolormesh(*args, **kwargs)
        self.axeC.axis("off")
        self.axeC.set_aspect("equal")
        self.axeC.set_xticks([])
        self.axeC.set_yticks([])
        return self.surfaceH

    def contour(self, *args, **kwargs):
        """2D contour plot"""
        self.surfaceH = self.axeC.contour(*args, **kwargs)
        return self.surfaceH

    def scatter(self, *args, **kwargs):
        """Plot scattered data"""
        self.surfaceH = self.axeC.scatter(*args, **kwargs)
        return self.surfaceH

    def colorbar(self, *args, **kwargs):
        """Add colorbar to figure"""
        self.figH.colorbar(*args, self.surfaceH, ax=self.axeC, **kwargs)

    #        self.axeC.colorbar(*args,**kwargs)
    def axis(self, *args, **kwargs):
        """Access axis properties such as 'off'"""
        self.axeC.axis(*args, **kwargs)

    def axis_aspect(self, *args, **kwargs):
        """Access axis aspect ration"""
        self.axeC.set_aspect(*args, **kwargs)

    def grid(self, *args, color="grey", alpha=0.2, **kwargs):
        """Access axis aspect ration"""
        self.axeC.grid(*args, color=color, alpha=alpha, **kwargs)

    def annotate(self, *args, **kwargs):
        """Annotation to figure"""
        self.axeC.annotate(*args, **kwargs)

    def text(self, *args, **kwargs):
        """Text to figure"""
        self.axeC.text(*args, **kwargs)

    def title(self, *args, **kwargs):
        """Set title for current axis"""
        self.axeC.set_title(*args, **kwargs)

    def xscale(self, *args, **kwargs):
        """Set x-axis scaling"""
        self.axeC.set_xscale(*args, **kwargs)

    def yscale(self, *args, **kwargs):
        """Set y-axis scaling"""
        self.axeC.set_yscale(*args, **kwargs)

    def xlabel(self, *args, **kwargs):
        """Set xlabel for current axis"""
        self.axeC.set_xlabel(*args, **kwargs)

    def ylabel(self, *args, **kwargs):
        """Set ylabel for current axis"""
        self.axeC.set_ylabel(*args, **kwargs)

    def xlim(self, xmin=np.inf, xmax=-np.inf):
        """Set limits for current x-axis: fig.xlim(0,1) or fig.xlim()"""
        try:
            if np.size(xmin) == 2:
                xmax = xmin[1]
                xmin = xmin[0]
            elif xmin == np.inf and xmax == -np.inf:
                for iline in self.axeC.lines:
                    xdata = iline.get_xdata()
                    xmin = np.minimum(xmin, np.nanmin(xdata))
                    xmax = np.maximum(xmax, np.nanmax(xdata))
            if version.parse(matplotlib.__version__) >= version.parse("3"):
                if np.isfinite(xmin):
                    self.axeC.set_xlim(left=xmin)
                if np.isfinite(xmax):
                    self.axeC.set_xlim(right=xmax)
            else:
                if np.isfinite(xmin):
                    self.axeC.set_xlim(xmin=xmin)
                if np.isfinite(xmax):
                    self.axeC.set_xlim(xmax=xmax)
        except Exception as excpt:
            print("classfig.xlim() throws exception:")
            print(excpt)
            # pass

    def ylim(self, ymin=np.inf, ymax=-np.inf):
        """Set limits for current y-axis: fig.ylim(0,1) or fig.ylim()"""
        try:
            if np.size(ymin) == 2:
                ymax = ymin[1]
                ymin = ymin[0]
            elif ymin == np.inf and ymax == -np.inf:
                for iline in self.axeC.lines:
                    ydata = iline.get_ydata()
                    ymin = np.minimum(ymin, np.nanmin(ydata))
                    ymax = np.maximum(ymax, np.nanmax(ydata))
            if version.parse(matplotlib.__version__) >= version.parse("3"):
                if np.isfinite(ymin):
                    self.axeC.set_ylim(bottom=ymin)
                if np.isfinite(ymax):
                    self.axeC.set_ylim(top=ymax)
            else:
                if np.isfinite(ymin):
                    self.axeC.set_ylim(ymin=ymin)
                if np.isfinite(ymax):
                    self.axeC.set_ylim(ymax=ymax)
        except Exception as excpt:
            print("classfig.ylim() throws exception:")
            print(excpt)
            # pass

    def legend(self, *args, labels=None, **kwargs):
        """Insert legend based on labels given in plot(x,y,label='Test1') etc."""
        if labels is not None:
            ilabel = 0
            for iline in self.axeC.lines:
                iline.set_label(labels[ilabel])
                ilabel += 1
        handles, labels = self.axeC.get_legend_handles_labels()
        if np.size(self.axeC.lines) != 0 and len(labels) != 0:
            self.axeC.legend(*args, **kwargs)

    def legend_entries(self):
        """Returns handle and labels of legend"""
        handles, labels = self.axeC.get_legend_handles_labels()
        return handles, labels

    def legend_count(self):
        """Return number of legend entries"""
        handles, labels = self.axeC.get_legend_handles_labels()
        return np.size(handles)

    def set_cycle(self, color_seq=False, linestyle_seq=False):  # ,linewidth=False):
        """Call to set color and linestyle cycle (will be used in this order)"""
        if color_seq is False:
            color_seq = self.presets["color_seq"]
        if linestyle_seq is False:
            linestyle_seq = self.presets["linestyle_seq"]

        # generate cycle from color_seq and linestyle_seq
        color_list = [
            self.colors[icolor] for icolor in color_seq if icolor in self.colors
        ]
        cyc_color = np.tile(color_list, (np.size(self.presets["linestyle_seq"]), 1))
        cyc_linestyle = np.repeat(linestyle_seq, np.shape(color_list)[0])
        try:
            matplotlib.rc(
                "axes",
                prop_cycle=(
                    cycler("color", cyc_color) + cycler("linestyle", cyc_linestyle)
                ),
            )
            if hasattr(self, "axeC"):
                self.axeC.set_prop_cycle(
                    cycler("color", cyc_color) + cycler("linestyle", cyc_linestyle)
                )
        except Exception as excpt:
            print("classfig.__init__(): Cannot set cycle for color and linestyle")
            print(excpt)

    def set_parameters(self):
        """Set useful figure parameters, called automatically by save
        and show function
        """
        # try:
        #     if (
        #         self.axeC.get_xscale() != "log"
        #     ):  # Otherwise xticks get missing on saving/showing- seems to be a bug
        #         self.axeH.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(7))
        # except:
        #     pass
        try:
            self.figH.tight_layout()
        except Exception as excpt:
            print("classfig.set_parameters(): Tight layout cannot be set!")
            print(excpt)

        if self.subplot_hspace is not None and self.subplot_nrows > 1:
            self.figH.subplots_adjust(hspace=self.subplot_hspace)
        if self.subplot_vspace is not None and self.subplot_ncols > 1:
            self.figH.subplots_adjust(vspace=self.subplot_vspace)

    def watermark(self, img, *args, xpos=100, ypos=100, alpha=0.15, zorder=1, **kwargs):
        """Include watermark image to plot"""
        if os.path.isfile(img):
            self.figH.figimage(
                img, xpos, ypos, alpha=alpha, zorder=zorder, *args, **kwargs
            )
        else:
            print("classfig.watermark(): File not found")

    def show(self):
        """Show figure in interactive console (similar to save)"""
        self.set_parameters()
        matplotlib.pyplot.show()  # block=False)

    def save(self, filename, *args, **kwargs):
        """Save figure to png, pdf: fig.save('test.png',600,'pdf')"""
        dpi = 300
        fileparts = filename.split(".")
        fileformat = set()
        fileformat.add(fileparts[-1])
        filename = filename.replace("." + fileparts[-1], "")
        for attribute in args:
            if isinstance(attribute, int):
                dpi = attribute
            else:
                fileformat.add(attribute)
        if "dpi" not in kwargs:
            kwargs["dpi"] = dpi

        self.set_parameters()
        for iformat in fileformat:
            try:
                pathlib.Path(os.path.dirname(filename)).mkdir(
                    parents=True, exist_ok=True
                )
                self.figH.savefig(filename + "." + iformat, **kwargs)
            except Exception as excpt:
                print(
                    f"classfig.save(): Figure cannot be saved to {filename}.{iformat}"
                )
                print(excpt)
        if self.figshow:
            matplotlib.pyplot.show()  # block=False)
        else:
            matplotlib.pyplot.draw()

    def clear(self, *args, **kwargs):
        """Clear figure content in order to reuse figure"""
        self.figH.clf(*args, **kwargs)

    def close(self, *args, **kwargs):
        """Close figure"""
        #        self.figH.close(*args,**kwargs)
        try:
            matplotlib.pyplot.close(self.figH)
        except Exception as excpt:
            print("classfig.close(): Figure cannot be closed")
            print(excpt)


# %%
def unit(value=0, unit="", precision=3, verbose=False, filecompatible=False):
    """Formatting of values for scientific use of SI units

    from classfig import unit
    unit(0.1,"m") == "100mm"
    unit(200e-9,"_s") == "200_ns"
    unit(1.000213, "m", precision=5) == "1000.2mm"
    unit(1.0001, " m") == "1 m"  # space
    unit(1.0001, "_m") == "1_m"  # space
    unit(0.911, "%") == "91.1%"  # percent
    unit(1001, "dB") == "30dB"  # dB
    unit(1030e-9, "!m") == "1p03um"

    The following wildcards can be used in the argument unit:
    - "dB" converts to decibels
    - "%" converts to percent
    - " " between number and unit
    - "_" between number and unit
    - "!" generates a filename compatible string "2p43nm"

    verbose=True returns additional information for scaling of vectors"""

    # preprocess input
    try:
        val = np.squeeze(value).astype(float)
    except Exception as excpt:
        print("Cannot convert input to float")
        print(excpt)
        return value

    # process hidden options
    separator = ""
    if " " in unit:
        separator = " "
        unit = unit.replace(" ", "")
    elif "_" in unit:
        separator = "_"
        unit = unit.replace("_", "")

    if "!" in unit:
        filecompatible = True
        unit = unit.replace("!", "")

    sign = 1
    if val < 0:
        sign = -1
    val *= sign

    if type(precision) not in [float, int]:
        with np.errstate(divide="ignore", invalid="ignore"):
            exponent = np.floor(np.log10(np.min(np.abs(np.diff(precision)))))
        precision = np.abs(exponent - np.floor(np.log10(val))) + 1
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            exponent = np.floor(np.log10(val))

    if precision == 4 or precision == 5:
        # 1032.1 nm instead of 1.0321 µm
        exponent -= 3

    prefix = ""
    mult = 0

    if unit == "dB":
        string = (
            ("{0:." + str(int(precision)) + "g}").format(10 * np.log10(val))
            + separator
            + unit
        )
    elif unit == "%":
        string = (
            ("{0:." + str(int(precision)) + "g}").format(sign * 100 * val)
            + separator
            + unit
        )
    else:
        # exponent = floor(log10(val));
        # error: calculation leads to 1e+3 µW instead of 1mW for 9.999e-4 input
        # error: Calculation gives infinity for 0W

        if exponent <= -19:
            prefix = ""
            mult = 0
        elif exponent <= -16:
            prefix = "a"
            mult = -18
        elif exponent <= -13:
            prefix = "f"
            mult = -15
        elif exponent <= -10:
            prefix = "p"
            mult = -12
        elif exponent <= -7:
            prefix = "n"
            mult = -9
        elif exponent <= -4:
            prefix = "µ"
            mult = -6
        elif exponent <= -1:
            prefix = "m"
            mult = -3
        elif exponent <= 2:
            prefix = ""
            mult = 0
        elif exponent <= 5:
            prefix = "k"
            mult = 3
        elif exponent <= 8:
            prefix = "M"
            mult = 6
        elif exponent <= 11:
            prefix = "G"
            mult = 9
        elif exponent <= 14:
            prefix = "T"
            mult = 12
        elif exponent <= 17:
            prefix = "P"
            mult = 15

        string = (
            ("{0:." + str(int(precision)) + "g}").format(sign * val * 10 ** (-mult))
            + separator
            + prefix
            + unit
        )
        if "e+03" in string:
            string = (
                ("{0:." + str(int(precision + 1)) + "g}").format(
                    sign * val * 10 ** (-mult)
                )
                + separator
                + prefix
                + unit
            )

    # Convert string to be filename compatible
    if filecompatible:
        string = string.replace("µ", "u")
        string = string.replace(".", "p")
        string = string.replace("/", "p")
        string = string.replace(" ", "_")

    if verbose:
        # Return string, multiplier and prefix
        return string, mult, prefix
    else:
        # Return just the formatted string
        return string


# %%

if __name__ == "__main__":
    fig = classfig()
    fig.plot()
    fig.show()
