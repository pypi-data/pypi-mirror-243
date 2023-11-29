"""
Plot single lightcurves or all lightcurves of a given status.

* :func:`plot_sample_lightcurves` plots all lightcurves of a given status
* :func:`plot_single_lightcurve` plots a single lightcurve
* :func:`make_lightcurve_plot` is the actual plotting function
"""

import os.path

import matplotlib.pyplot as plt
import matplotlib as mpl
import logging
import pandas as pd
from timewise.wise_data_base import WISEDataBase

from timewise_sup.meta_analysis.flux import get_ir_flux, get_ir_flux_index, flux_key, flux_err_key
from timewise_sup.plots import plots_dir, bandcolors


logger = logging.getLogger(__name__)


def plot_sample_lightcurves(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: str,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
):
    """
    Plot all lightcurves of a given status.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: WISE data object
    :type wise_data: WISEDataBase
    :param status: status of the lightcurves to plot
    :type status: str
    :func:`timewise_sup.meta_analysis.ztf.get_ztf_lightcurve` or
    :func:`timewise_sup.meta_analysis.ztf.download_ztffp_per_status` before
    :param service: serice with which the lightcurves were downloaded by ``timewise`` (default: ``tap``)
    :type service: str, optional
    :param load_from_bigdata_dir: whether to load the lightcurves from the bigdata directory (default: ``False``)
    :type load_from_bigdata_dir: bool, optional
    """
    wise_lcs = get_ir_flux(
        base_name=base_name,
        database_name=database_name,
        wise_data=wise_data,
        status=status,
        service=service,
        load_from_bigdata_dir=load_from_bigdata_dir
    )

    for index, lc_dict in wise_lcs.items():
        logger.debug(f"index {index}")
        wise_lc = pd.DataFrame.from_dict(lc_dict)

        fig, ax = make_lightcurve_plot(wise_lc)

        d = plots_dir("baseline_subtracted_lightcurves", base_name)
        fn = os.path.join(d, status, f"{index}.pdf")

        d = os.path.dirname(fn)
        if not os.path.isdir(d):
            os.makedirs(d)

        logger.debug(f"saving under {fn}")
        fig.savefig(fn)
        plt.close()


def plot_single_lightcurve(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: str,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """
    Plot a single lightcurve.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: WISE data object
    :type wise_data: WISEDataBase
    :param index: index of the lightcurve
    :type index: str
    :param service: service used to download the lightcurves, default "tap", passed to :func:`get_ir_flux_index`
    :type service: str, optional
    :param load_from_bigdata_dir: load from bigdata directory, defaults to False, passed to :func:`get_ir_flux_index`
    :type load_from_bigdata_dir: bool, optional
    :return: figure and axes
    :rtype: tuple[mpl.figure.Figure, mpl.axes.Axes]
    """

    wise_lc = pd.DataFrame.from_dict(get_ir_flux_index(
        base_name=base_name,
        database_name=database_name,
        wise_data=wise_data,
        index=index,
        service=service,
        load_from_bigdata_dir=load_from_bigdata_dir
    )[str(index)], orient="columns")

    return make_lightcurve_plot(wise_lc)


def make_lightcurve_plot(
        wise_lc: pd.DataFrame,
        ax: mpl.axes.Axes | None = None,
        x_key: str = "mean_mjd",
        y_key: str = flux_key,
        y_err_key: str = flux_err_key,
        ylabel: str = r"$\nu$ F$_{\nu}$ [erg s$^{-1}$ cm$^{-2}$]"
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """
    Make a lightcurve plot.

    :param wise_lc: The WISE lightcurve
    :type wise_lc: pd.DataFrame
    :param ax: axes to plot on, defaults to creating a new figure
    :type ax: mpl.axes.Axes, optional
    :param x_key: key for the x axis, defaults to ``mean_mjd``
    :type x_key: str, optional
    :param y_key: key for the y axis, defaults to ``flux_key``
    :type y_key: str, optional
    :param y_err_key: key for the y error, defaults to ``flux_err_key``
    :type y_err_key: str, optional
    :param ylabel: label for the y axis, defaults to ``r"$\nu$ F$_{\nu}$ [erg s$^{-1}$ cm$^{-2}$]"``
    :type ylabel: str, optional
    :return: figure and axes
    :rtype: tuple[mpl.figure.Figure, mpl.axes.Axes]
    """

    fig, _ax = plt.subplots() if ax is None else (plt.gcf(), ax)  # type: mpl.figure.Figure, mpl.axes.Axes

    for b in ["W1", "W2"]:
        _ax.errorbar(
            wise_lc[x_key],
            wise_lc[f"{b}_{y_key}"],
            yerr=wise_lc[f"{b}_{y_err_key}"],
            marker='s',
            ms=3,
            color=bandcolors[b],
            label=f"WISE {b}",
            ls="",
            zorder=5,
            capsize=2
        )

    _ax.set_ylabel(ylabel)
    _ax.grid()
    _ax.legend()

    return fig, _ax
