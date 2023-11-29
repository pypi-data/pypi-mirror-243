"""
Calculate the IR energy of the flares. This is done by integrating the luminosity over the duration of the flare.

The IR energy is calculated and stored in a json file. The file is named
ir_eng_status{status}.json, where status is the status of the flare. The file is stored in the directory
`timewise_sup_data/{base_name}`. If the file already exists, it is loaded from there. If it does not exist, it is
calculated and stored there.

* :func:`ir_energy_integral` calculates the IR energy for a given light curve
* :func:`calculate_ir_energy` calculates the IR energy for a given status
* :func:`get_ir_energy_status` calculates the IR energy for a given status
* :func:`get_ir_energy_index` calculates the IR energy for a given index

"""

import logging
import os
import json
from collections.abc import Mapping
import numpy as np
import pandas as pd
from scipy import integrate
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index, Status
from timewise_sup.meta_analysis.luminosity import (
    get_ir_luminosities,
    luminosity_key,
    luminosity_err_key,
    ref_time_key,
    get_ref_time
)
from timewise_sup.meta_analysis.integrate_time import time_integral


logger = logging.getLogger(__name__)

ir_energy_key = "ir_energy_erg"
ir_energy_err_key = "ir_energy_erg_err"


def calculate_ir_energy(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
        redshifts: pd.DataFrame | None = None,
) -> dict:
    """
    Calculate the IR energy of the flares. This is done by integrating the luminosity over the duration of the flare.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param status: status of the flare
    :type status: Status
    :param redshifts:
        redshift of the object, defaults to getting the redshift from the AMPEL catalog crossmatch,
        needs keys `z` and `z_unc`
    :type redshifts: pandas.DataFrame | None
    :return: dictionary with the index as key and the IR energy as value
    :rtype: dict
    """
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    ids = database_connector.get_ids(status)
    indices = np.atleast_1d(ids)
    logger.info(f"calculating luminosities for {len(indices)} objects")
    luminosity_dict = get_ir_luminosities(base_name, database_name, wise_data, status, redshifts=redshifts)
    excess_mjd = database_connector.get_excess_mjd(indices)

    engs = {}  # type: dict[str, dict[str, float] | None]

    for k, lum_info in luminosity_dict.items():

        if lum_info is None:
            logger.warning(f"no luminosity information for {k}. Can not calculate IR energy.")
            engs[k] = None
            continue

        ref_time = lum_info["ref_time_mjd"]
        lc = pd.DataFrame(lum_info["lightcurve"])
        t_start = excess_mjd.loc[k, ["W1_excess_start_mjd", "W2_excess_start_mjd"]].min() - ref_time
        t_end = excess_mjd.loc[k, ["W1_excess_end_mjd", "W2_excess_end_mjd"]].max() - ref_time
        integral = time_integral(
            lc=lc,
            key=luminosity_key,
            err_key=luminosity_err_key,
            t_start=t_start,
            t_end=t_end,
            time_key=ref_time_key,
        )

        ieng = dict()
        for b in ["W1", "W2"]:
            ieng[f"{b}_{ir_energy_key}"] = integral[f"{b}_{luminosity_key}_integrated"]
            ieng[f"{b}_{ir_energy_err_key}"] = integral[f"{b}_{luminosity_key}_integrated_err"]
        ieng[ir_energy_key] = np.sum([ieng[f"{b}_{ir_energy_key}"] for b in ["W1", "W2"]])
        ieng[ir_energy_err_key] = np.sqrt(np.sum([ieng[f"{b}_{ir_energy_err_key}"] ** 2 for b in ["W1", "W2"]]))
        ieng["ir_energy_is_lower_limit"] = bool(np.any([excess_mjd.loc[k, f"{b}_flare_ended"] for b in ["W1", "W2"]]))
        ieng["z"] = lum_info["z"]
        ieng["z_err"] = lum_info["z_err"]
        engs[k] = ieng

    return engs


def get_ir_energy_status(
        base_name: str,
        database_name: str,
        status: Status,
        redshifts: pd.DataFrame | None = None,
        wise_data: WISEDataBase | None = None,
        force_new: bool = False,
) -> dict:
    """
    Get the IR energy of the flares per status. If the cache file `ir_eng_status{status}.json` exists, it is loaded from there.
    If it does not exist, it is calculated by :func:`calculate_ir_energy` and stored there.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param status: status for which the IR energy should be calculated
    :type status: Status
    :param redshifts:
        redshift of the object, defaults to getting the redshift from the AMPEL catalog crossmatch,
        needs keys `z` and `z_unc`
    :type redshifts: pandas.DataFrame | None
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param force_new: if True, the IR energy is calculated and stored in the cache file, even if it already exists
    :type force_new: bool
    :return: dictionary with the index as key and the IR energy as value
    :rtype: dict
    """
    logger.info(f"getting bolometric luminosities for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"ir_eng_status{status}.json")

    if (not os.path.isfile(fn)) or force_new:

        if wise_data is None:
            raise ValueError("wise_data must be given when calculating IR energies!")
        else:
            logger.debug(f"No file {fn}.")
            logger.info("Making bolometric luminosities")
            engs = calculate_ir_energy(
                base_name=base_name,
                database_name=database_name,
                wise_data=wise_data,
                status=status,
                redshifts=redshifts,
            )

        with open(fn, "w") as f:
            json.dump(engs, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            engs = json.load(f)

        if redshifts is None:
            connector = DatabaseConnector(base_name=base_name, database_name=database_name)
            indices = connector.get_ids(status)
            redshifts = connector.get_redshift(indices)

        for i, eng_info in engs.items():
            if eng_info is None:
                logger.warning(f"missing luminosity for {i}")

            elif eng_info["z"] != redshifts.loc[i, "z"]:
                raise ValueError(f"redshift mismatch for {i}: {eng_info['z']} != {redshifts.loc[i, 'z']}")

    return engs


def get_ir_energy_index(
        base_name: str,
        database_name: str,
        index: Index,
        wise_data: WISEDataBase,
        forcenew: bool = False,
) -> dict:
    """
    Get the IR energy of the flares per index by getting the status and calling :func:`get_ir_energy_status`
    for each status.

    :param base_name:
    :type base_name: str
    :param database_name:
    :type database_name: str
    :param index: index of the lightcurve
    :type index: Index
    :param forcenew: if True, the IR energy is calculated and stored in the cache file, even if it already exists
    :type forcenew: bool
    :return: dictionary with the index as key and the IR energy as value
    :rtype: dict
    """

    statuses = DatabaseConnector(base_name=base_name, database_name=database_name).get_status(index)

    engs_all = dict()

    for status in statuses.status.unique():
        eng = get_ir_energy_status(base_name, database_name, status, wise_data, forcenew)
        selected_lums = {k: v for k, v in eng.items() if k in statuses.index[statuses.status == status]}
        engs_all.update(selected_lums)

    return engs_all
