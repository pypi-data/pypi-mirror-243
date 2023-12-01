"""
Module with functions to calculate the IR flux from the IR spectral flux densities.

* :func:`get_ban_nu` returns the frequency of a given band
* :func:`ir_flux_density_integral` integrates the flux density over the wavelength range of a given band
* :func: `calculate_ir_flux` calculates the IR flux for given indices
* :func:`get_ir_flux_index` get the calculated IR flux for given indices and cache them to disk
* :func:`get_ir_flux` get the IR flux for a given status
"""

import logging
import os
import json
import numpy as np
from tqdm import tqdm
from numpy import typing as npt
import pandas as pd
from astropy import units as u
from astropy import constants
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index, Status, jd_offset
from timewise_sup.meta_analysis.baseline_subtraction import get_lightcurves


logger = logging.getLogger(__name__)


flux_key = "nuFnu_erg_per_s_per_sqcm"
flux_err_key = "nuFnu_err_erg_per_s_per_sqcm"
band_wavelengths = {
    # from Wright et al. (2010) ( 10.1088/0004-6256/140/6/1868 )
    "W1": 3.4 * 1e-6 * u.m,
    "W2": 4.6 * 1e-6 * u.m,
}


def get_band_nu(band: str | u.Quantity) -> u.Quantity:
    """Returns the frequency of a given band"""
    wl = band_wavelengths[band] if isinstance(band, str) else band
    return constants.c / wl


def flux_integral(
        spectral_flux_density: list[float],
        spectral_flux_density_unit: str,
        band: str | u.Quantity,
        out_unit: str = "erg s-1 cm-2"
) -> npt.NDArray:
    """
    Calculates the flux density value of a given spectral flux density. The flux density is calculated by multiplying
    the spectral flux density with the frequency of the given band.

    :param spectral_flux_density:
    :type spectral_flux_density: list[float]
    :param spectral_flux_density_unit:
    :type spectral_flux_density_unit: str
    :param band: either of "W1" or "W2" or the wavelength of the band
    :type band: str | astropy.units.Quantity
    :param out_unit:
    :type out_unit: str
    :return:
    """
    _flux = np.array(spectral_flux_density) * u.Unit(spectral_flux_density_unit)
    nu = get_band_nu(band)
    return np.array(u.Quantity(_flux * nu).to(out_unit).value)


def calculate_ir_flux(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
) -> dict:
    """
    Calculates the IR flux for a given index. The IR flux is calculated by multiplying the flux density with the
    frequency of the given band.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param index: index of the object
    :type index: Index
    :param service: service to use for the TAP query, defaults to "tap", passed to :func:`get_lightcurves`
    :type service: str, optional
    :param load_from_bigdata_dir: load from the bigdata directory, defaults to False, passed to :func:`get_lightcurves`
    :type load_from_bigdata_dir: bool, optional
    :return: dictionary with the index as key and the IR fluxes as value
    :rtype: dict
    """
    indices = tuple(np.atleast_1d(index).astype(int))
    logger.info(f"calculating flux for {len(indices)} objects")

    lcs = get_lightcurves(base_name, database_name, wise_data, indices,
                          service=service, load_from_bigdata_dir=load_from_bigdata_dir)
    logger.debug(f"got {len(lcs)} lightcurves")
    lcs_with_fluxes = dict()

    for i, lc_dict in lcs.items():
        lc_in = pd.DataFrame.from_dict(lc_dict, orient="columns")
        lc_out = lc_in[["mean_mjd"]].copy()

        for b in ["W1", "W2"]:
            lc_out[f"{b}_{flux_key}"] = flux_integral(
                lc_in[f"{b}_diff_mean_flux_density"],
                spectral_flux_density_unit="mJy",
                band=b,
                out_unit="erg s-1 cm-2"
            )
            lc_out[f"{b}_{flux_err_key}"] = flux_integral(
                lc_in[f"{b}_diff_flux_density_rms"],
                spectral_flux_density_unit="mJy",
                band=b,
                out_unit="erg s-1 cm-2"
            )

        lcs_with_fluxes[str(i)] = lc_out.to_dict()

    return lcs_with_fluxes


def get_ir_flux(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
        force_new: bool = False,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
) -> dict:
    """
    Get the IR flux of the flares per status. If the cache file `flux_ir_lcs_status{status}.json` exists,
    it is loaded from there. If it does not exist, it is calculated by :func:`calculate_ir_flux` and stored there.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param status: status for which the IR flux should be calculated
    :type status: Status
    :param force_new: if True, the IR flux is calculated even if the cache file exists, defaults to False
    :type force_new: bool, optional
    :param service: service to use for the TAP query, defaults to "tap", passed to :func:`get_lightcurves`
    :type service: str, optional
    :param load_from_bigdata_dir: load from the bigdata directory, defaults to False, passed to :func:`get_lightcurves`
    :type load_from_bigdata_dir: bool, optional
    :return: dictionary with the index as key and the IR fluxes as value
    :rtype: dict
    """
    logger.info(f"getting fluxes for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"flux_ir_lcs_status{status}.json")

    if (not os.path.isfile(fn)) or force_new:
        logger.debug(f"No file {fn}")
        logger.info("calculating fluxes")

        database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
        indices = database_connector.get_ids(status)
        lcs = calculate_ir_flux(
            base_name,
            database_name,
            wise_data,
            indices,
            service=service,
            load_from_bigdata_dir=load_from_bigdata_dir
        )

        logger.debug(f"writing to {fn}")
        with open(fn, "w") as f:
            json.dump(lcs, f)

    else:
        logger.debug(f"reading from {fn}")
        with open(fn, "r") as f:
            lcs = json.load(f)

    return lcs


def get_ir_flux_index(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
) -> dict:
    """
    Get the IR flux of the flares by index. Checks the statuses of the flares and loads the respective files
    (or creates them) with :func:`get_ir_flux`.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param index: index of the object
    :type index: Index
    :param service: service to use for the TAP query, defaults to "tap", passed to :func:`get_lightcurves`
    :type service: str, optional
    :param load_from_bigdata_dir: load from the bigdata directory, defaults to False, passed to :func:`get_lightcurves`
    :type load_from_bigdata_dir: bool, optional
    :return: dictionary with the index as key and the IR fluxes as value
    :rtype: dict
    """
    _index = np.atleast_1d(index).astype(int)
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    statuses = database_connector.get_status(list(_index))

    fluxes = dict()
    for status in statuses.status.unique():
        m = statuses.status == status
        status_ir_fluxes = get_ir_flux(base_name, database_name, wise_data, status,
                                       service=service, load_from_bigdata_dir=load_from_bigdata_dir)
        fluxes.update({str(i): status_ir_fluxes[str(i)] for i in _index[m]})

    return fluxes


def get_max_flux(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
) -> pd.DataFrame:
    """
    Get the maximum flux of the flares by index. Gets the time of the maximum flux from the database and
    returns the flux at that time.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param index: index of the object
    :type index: Index
    :param service: service to use for the TAP query, defaults to "tap", passed to :func:`get_lightcurves`
    :type service: str, optional
    :param load_from_bigdata_dir: load from the bigdata directory, defaults to False, passed to :func:`get_lightcurves`
    :type load_from_bigdata_dir: bool, optional
    :return: dictionary with the index as key and the maximum flux as value
    :rtype: dict
    """

    logger.info(f"getting max flux for {len(np.atleast_1d(index))} objects of {base_name}")
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    jd_of_max_flux = database_connector.get_peak_time_jd(index)
    mjd_of_max_flux = jd_of_max_flux + jd_offset
    fluxes = get_ir_flux_index(base_name, database_name, wise_data, index,
                               service=service, load_from_bigdata_dir=load_from_bigdata_dir)
    max_fluxes = {}
    for i in tqdm(index, desc="getting max fluxes"):
        lc = pd.DataFrame(fluxes[str(i)])
        i_max_fluxes = {}
        for b in ["W1", "W2"]:
            m = (lc.mean_mjd - mjd_of_max_flux.loc[str(i), f"max_mag_jd_{b}"]).abs() < 1e-9
            i_max_fluxes[f"{b}_max_flux"] = lc[m][f"{b}_{flux_key}"].values[0]
            i_max_fluxes[f"{b}_max_flux_err"] = lc[m][f"{b}_{flux_err_key}"].values[0]

        max_fluxes[str(i)] = i_max_fluxes

    return pd.DataFrame.from_dict(max_fluxes, orient="index")
