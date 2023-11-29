"""
Functions to perform integration of a lightcurve over the duration of the flare

* :func:`time_integral` calculates the integral of a lightcurve over the duration of the flare
"""

import logging
import pandas as pd
from scipy import integrate
import numpy as np

from timewise_sup.mongo import DatabaseConnector, Index


logger = logging.getLogger(__name__)


def time_integral(
        lc: pd.DataFrame,
        key: str,
        err_key: str,
        t_start: float,
        t_end: float,
        time_key: str = "mean_mjd",
) -> dict[str, float]:
    mjd = lc[time_key]
    integral = {}

    for b in ["W1", "W2"]:
        mask = (mjd >= t_start) & (mjd <= t_end)
        fit_val = lc[f"{b}_{key}"][mask]
        fit_mjd = mjd[mask]

        # integrate using trapezoidal rule
        i_integral = integrate.trapezoid(fit_val, fit_mjd * 24 * 3600)
        integral[f"{b}_{key}_integrated"] = i_integral

        # try to estimate the error:
        # maximum of difference when calculating the integral with the upper and lower error
        fit_val_err = lc[f"{b}_{err_key}"][mask]
        fit_val_err_up = fit_val + fit_val_err
        fit_val_err_lo = fit_val - fit_val_err
        errors = np.array([integrate.trapezoid(e, fit_mjd * 24 * 3600) for e in [fit_val_err_up, fit_val_err_lo]])
        i_integral_err = max(np.abs(i_integral - errors))
        integral[f"{b}_{key}_integrated_err"] = i_integral_err

    return integral


def get_flare_time(
        base_name: str,
        database_name: str,
        index: Index,
) -> pd.DataFrame:
    """
    Get the flare time for a given index. The start and end times are the median of the start and end of the
    IR excess periods in W1 and W2. The lower limit is True if the flare di not end in W1 or W2.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param index: index of the object
    :type index: int
    :return: flare time
    :rtype: dict
    """
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    excess_times = database_connector.get_excess_mjd(index=index)
    start_times = excess_times[["W1_excess_start_mjd", "W2_excess_start_mjd"]].median(axis=1)
    end_times = excess_times[["W1_excess_end_mjd", "W2_excess_end_mjd"]].median(axis=1)
    lower_limit = ~excess_times[["W1_flare_ended", "W2_flare_ended"]].all(axis=1)
    return pd.DataFrame({
        "start_time": start_times,
        "end_time": end_times,
        "lower_limit": lower_limit,
    })
