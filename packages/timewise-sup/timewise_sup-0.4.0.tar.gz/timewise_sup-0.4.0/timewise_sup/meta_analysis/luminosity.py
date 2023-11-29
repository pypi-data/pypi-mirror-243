"""
Calculates the IR luminosities of the lightcurves in the database.

* :func:`get_band_nu` returns the frequency of a given band
* :func:`nuFnu` calculates the flux density value of a given spectral flux density
* :func:`calculate_ir_luminosities` calculates the IR luminosities for a given index
* :func:`get_ir_luminosities` calculates the IR luminosities for a given status
"""

import logging
import os
import json

import numpy as np
import pandas as pd
from astropy import units as u
from astropy.cosmology import Planck18
from astropy.uncertainty import normal
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index, Status, jd_offset
from timewise_sup.meta_analysis.flux import get_ir_flux_index, flux_key, flux_err_key


logger = logging.getLogger(__name__)

luminosity_key = "ir_luminosity_erg_per_s"
luminosity_err_key = "ir_luminosity_err_erg_per_s"
ref_time_key = "source_frame_time"


def get_ref_time(
        base_name: str,
        database_name: str,
        index: Index,
):
    connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    peak_times = connector.get_peak_time_jd(index)
    mean_peak_time = peak_times.mean(axis=1)
    return mean_peak_time + jd_offset


def calculate_ir_luminosities(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        redshift: pd.Series,
        redshift_err: pd.Series,
) -> dict:
    """
    Calculates the IR luminosities for a given index. The IR luminosity is calculated by multiplying the flux density
    with the area of the sphere with the radius of the luminosity distance. The luminosity distance is calculated
    using the Planck18 cosmology. The area is calculated using the formula for the surface area of a sphere.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param index: index of the object
    :type index: Index
    :param redshift: redshift of the object
    :type redshift: pd.Series
    :param redshift_err: redshift error of the object
    :type redshift_err: pd.Series
    :return: dictionary with the index as key and the IR luminosities as value
    :rtype: dict
    """
    indices = tuple(np.atleast_1d(index).astype(int))
    logger.info(f"calculating luminosities for {len(indices)} objects")

    if len(indices) != len(redshift):
        raise ValueError("redshift and index must have the same length!")

    lcs = get_ir_flux_index(base_name, database_name, wise_data, indices)
    logger.debug(f"got {len(lcs)} lightcurves")

    ref_times = get_ref_time(base_name, database_name, indices)
    ref_times.index = ref_times.index.astype(str)
    lcs_with_luminosities = dict()

    # avoid SettingWithCopyWarning which falsely flags something like lc[ref_time_key] = ...
    with pd.option_context('mode.chained_assignment', None):

        for i, lc_dict in lcs.items():
            lc_in = pd.DataFrame.from_dict(lc_dict, orient="columns")
            lc = lc_in[["mean_mjd"]]

            iredshift = redshift[i]
            iredshift_err = redshift_err[i]

            one_plus_z = 1 + iredshift
            one_plus_z_err = iredshift_err if not np.isnan(iredshift_err) else 0
            one_by_one_plus_z = 1 / one_plus_z

            dl = Planck18.luminosity_distance(iredshift)
            area = 4 * np.pi * dl ** 2

            # estimate the uncertainty of the luminosity distance by sampling the redshift distribution
            # if the uncertainty of the redshift is given
            if not np.isnan(iredshift_err):
                iredshift_dist = normal(iredshift, std=iredshift_err, n_samples=10000)
                lum_dist_std = np.std(Planck18.luminosity_distance(iredshift_dist.distribution))
                area_unc = 8 * np.pi * dl * lum_dist_std
            else:
                area_unc = 0 * (u.Mpc ** 2)

            lc[ref_time_key] = (lc["mean_mjd"] - ref_times.loc[i]) * one_by_one_plus_z

            for b in ["W1", "W2"]:

                flux_val = u.Quantity(lc_in[f"{b}_{flux_key}"] * u.Unit("erg s-1 cm-2"))
                flux_valerr = u.Quantity(lc_in[f"{b}_{flux_err_key}"] * u.Unit("erg s-1 cm-2"))

                lum = u.Quantity(flux_val * area * one_plus_z).to("erg s-1").value
                lum_err = u.Quantity(
                    np.sqrt(
                        (flux_valerr * area * one_plus_z) ** 2
                        + (flux_val * area_unc * one_plus_z) ** 2
                        + (flux_val * area * one_plus_z_err) ** 2
                    )
                ).to("erg s-1").value

                lc[f"{b}_{luminosity_key}"] = lum
                lc[f"{b}_{luminosity_err_key}"] = lum_err

            lum_dict = {
                "lightcurve": lc.to_dict(),
                "z": iredshift,
                "z_err": iredshift_err,
                "ref_time_mjd": ref_times.loc[i]
            }

            lcs_with_luminosities[str(i)] = lum_dict

    logger.debug(f"calculated luminosities for {len(lcs_with_luminosities)} objects")
    return lcs_with_luminosities


def get_ir_luminosities(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
        force_new: bool = False,
        redshifts: pd.DataFrame | None = None,
) -> dict:
    """
    Calculates the IR luminosities of the lightcurves in the database for a given status. If the cache file
    `lum_ir_lcs_status{status}.json` exists, it is loaded from there. If it does not exist, it is calculated by
    :func:`calculate_ir_luminosities` and stored there.

    :param base_name: base name for storage directories
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: instance of WISEDataBase
    :type wise_data: WISEDataBase
    :param status: status for which the IR luminosities should be calculated
    :type status: Status
    :param force_new: if True, the luminosities are calculated even if the cache file exists
    :type force_new: bool
    :param redshifts:
        redshift of the object, defaults to getting the redshift from the AMPEL catalog crossmatch,
        needs keys `z` and `z_unc`
    :type redshifts: pandas.DataFrame | None
    :return: dictionary with the index as key and the IR luminosities as value
    :rtype: dict
    """

    logger.info(f"getting luminosities for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"lum_ir_lcs_status{status}.json")

    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    indices = database_connector.get_ids(status)

    if (not os.path.isfile(fn)) or force_new:
        logger.debug(f"No file {fn}")
        logger.info("calculating luminosities")

        if redshifts is None:
            redshifts = database_connector.get_redshift(indices)
            redshifts.rename(columns={"ampel_z": "z", "group_z_precision": "z_unc"}, inplace=True)

        lcs = calculate_ir_luminosities(
            base_name,
            database_name,
            wise_data,
            redshifts.index,
            redshifts["z"],
            redshifts["z_unc"]
        )

        missing_mask = ~pd.Index(indices).astype(str).isin(lcs.keys())
        if any(missing_mask):
            logger.warning(f"missing {missing_mask.sum()} lightcurves")
            missing_indices = np.array(indices)[missing_mask]
            for i in missing_indices:
                lcs[str(i)] = None

        logger.debug(f"writing to {fn}")
        with open(fn, "w") as f:
            json.dump(lcs, f)

    else:
        logger.debug(f"reading from {fn}")
        with open(fn, "r") as f:
            lcs = json.load(f)

        for i, lum_info in lcs.items():
            if lum_info is None:
                logger.warning(f"missing luminosity for {i}")

            elif (redshifts is not None) and (abs(1 - lum_info["z"] / redshifts.loc[i, "z"]) > 1e-7):
                raise ValueError(f"redshift mismatch for {i}: {lum_info['z']} != {redshifts.loc[i, 'z']}")

    return lcs


def get_ir_luminosities_index(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        force_new: bool = False,
        redshifts: pd.DataFrame | None = None,
) -> dict:
    logger.info(f"getting luminosities for {len(np.atleast_1d(index))} indices")
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    statuses = database_connector.get_status(index)
    unique_statuses = statuses.status.unique()
    logger.debug(f"unique statuses: {unique_statuses}")

    lums_all = dict()

    for status in unique_statuses:
        lums = get_ir_luminosities(base_name, database_name, wise_data, status, force_new, redshifts)
        selected_lums = {k: v for k, v in lums.items() if k in statuses.index[statuses.status == status]}
        lums_all.update(selected_lums)

    logger.debug(f"got {len(lums_all)} lightcurves")
    return lums_all


# def get_peak_ir_luminosity_index(
#         base_name: str,
#         database_name: str,
#         index: Index,
# ) -> dict:
#     logger.info(f"getting peak IR luminosities for index {ind} ({base_name})")
#     lcs = get_ir_luminosities(base_name, database_name, status)
#     logger.debug(f"got {len(lcs)} lightcurves")
#
#     peak_lum = dict()
#     for i, lc_dict in lcs.items():
#         lc = pd.DataFrame.from_dict(lc_dict, orient="columns")
#         peak_lum[i] = dict()
#         for b in ["W1", "W2"]:
#             arg = np.argmax(lc[f"{b}_luminosity_erg_per_s"])
#             peak_lum[i][f"{b}_peak_luminosity_erg_per_s"] = lc[f"{b}_luminosity_erg_per_s"][arg]
#             peak_lum[i][f"{b}_peak_luminosity_err_erg_per_s"] = lc[f"{b}_luminosity_err_erg_per_s"][arg]
#             peak_lum[i][f"{b}_peak_luminosity_mjd"] = lc["mean_mjd"][arg]

