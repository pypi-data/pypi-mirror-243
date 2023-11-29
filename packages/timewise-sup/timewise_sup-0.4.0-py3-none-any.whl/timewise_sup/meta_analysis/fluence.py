"""
Module with functions to calculate the IR fluence from the IR fluxes.

* :func:`ir_flux_integral` integrates the flux over the duration of the flare
* :func: `calculate_ir_fluence` calculates the IR fluence for given indices
* :func:`get_ir_fluence` get the calculated IR fluence for given status and cache them to disk
"""

import logging
import os
import json
import numpy as np
import pandas as pd
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Status
from timewise_sup.meta_analysis.flux import get_ir_flux, flux_key, flux_err_key
from timewise_sup.meta_analysis.integrate_time import time_integral, get_flare_time


logger = logging.getLogger(__name__)


fluence_key = "ir_fluence_erg_per_sqcm"
fluence_err_key = "ir_fluence_err_erg_per_sqcm"


def calculate_ir_fluence(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
) -> dict:
    """
    Calculate the IR fluence for a given status. The IR fluence is calculated by integrating the IR flux over the
    duration of the flare.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param status: status to calculate the IR fluence for
    :type status: Status
    :param service: service to use for the TAP query, defaults to "tap", passed to :func:`get_lightcurves`
    :type service: str, optional
    :param load_from_bigdata_dir: load from the bigdata directory, defaults to False, passed to :func:`get_lightcurves`
    :type load_from_bigdata_dir: bool, optional
    :return:
    """
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    ids = database_connector.get_ids(status)
    indices = np.atleast_1d(ids)
    logger.info(f"calculating fluence for {len(indices)} objects")
    lcs = get_ir_flux(base_name, database_name, wise_data, status,
                      service=service, load_from_bigdata_dir=load_from_bigdata_dir)
    flare_time = get_flare_time(base_name, database_name, indices)
    fluence = dict()

    for k, lc in lcs.items():
        i_fluence = time_integral(
            lc=pd.DataFrame.from_dict(lc, orient="columns"),
            key=flux_key,
            err_key=flux_err_key,
            t_start=flare_time.loc[str(k), "start_time"],
            t_end=flare_time.loc[str(k), "end_time"],
        )
        for b in ["W1", "W2"]:
            i_fluence[f"{b}_{fluence_key}"] = i_fluence.pop(f"{b}_{flux_key}_integrated")
            i_fluence[f"{b}_{fluence_err_key}"] = i_fluence.pop(f"{b}_{flux_key}_integrated_err")

        i_fluence["ir_fluence_is_lower_limit"] = bool(flare_time.loc[k, "lower_limit"])
        fluence[k] = i_fluence

    return fluence


def get_ir_fluence(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
        service: str = "tap",
        load_from_bigdata_dir: bool = False,
        force_new: bool = False
) -> dict:
    """
    Get the IR fluence for a given status. The IR fluence is calculated by integrating :func:`get_ir_flux` if it
    has not been calculated before. The results are cached to disk.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param status: status to calculate the IR fluence for
    :type status: Status
    :param service: service to use for the TAP query, defaults to "tap", passed to :func:`get_lightcurves`
    :type service: str, optional
    :param load_from_bigdata_dir: load from the bigdata directory, defaults to False, passed to :func:`get_lightcurves`
    :type load_from_bigdata_dir: bool, optional
    :param force_new: calculate fluence again, even if cache exists, defaults to False
    :type force_new: bool, optional
    :return: dictionary with the IR fluence for each index
    :rtype: dict
    """

    logger.info(f"getting fluxes for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"fluence_ir_status{status}.json")
    logger.info(f"getting IR fluence for status {status}")

    if os.path.exists(fn) and not force_new:
        logger.info(f"loading IR fluence from {fn}")
        with open(fn, "r") as f:
            fluence = json.load(f)

    else:
        logger.debug(f"No file {fn}")
        logger.info(f"calculating IR fluence")
        fluence = calculate_ir_fluence(
            base_name=base_name,
            database_name=database_name,
            wise_data=wise_data,
            status=status,
            service=service,
            load_from_bigdata_dir=load_from_bigdata_dir
        )
        logger.info(f"saving IR fluence to {fn}")
        with open(fn, "w") as f:
            json.dump(fluence, f)

    return fluence
