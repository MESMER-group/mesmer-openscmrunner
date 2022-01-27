# MESMER-OpenSCM Runner, land-climate dynamics group, S.I. Seneviratne
# Copyright (c) 2021-2022 MESMER-OpenSCM Runner contributors, listed in AUTHORS, and ETH Zurich.
# Licensed under the GNU General Public License v3.0 or later; see LICENSE or https://www.gnu.org/licenses/


import os.path

import scmdata
import xarray as xr
from openscm_units import unit_registry

from mesmer_openscmrunner.draw_realisations import (
    _draw_realisations_from_mesmer_file_and_openscm_output,
)


def test_create_realisations_from_pre_run_data(test_data_dir):
    mesmer_bundle_file = os.path.join(
        test_data_dir, "mesmer-bundles", "test-generic-mesmer-bundle.pkl"
    )

    magicc_output_dir = os.path.join(test_data_dir, "magicc-rcmip-phase-1-output")
    magicc_output_gsat = os.path.join(
        test_data_dir,
        magicc_output_dir,
        "rcmip-phase-1_magicc7.1.0.beta-canesm5-r1i1p1f1_world_surface-air-temperature-change.csv",
    )
    magicc_output_ohc = os.path.join(
        test_data_dir,
        magicc_output_dir,
        "rcmip-phase-1_magicc7.1.0.beta-canesm5-r1i1p1f1_world_heat-content-ocean.csv",
    )

    run_years = range(1850, 2100 + 1)
    scenarios_to_run = ["ssp126"]

    openscm_gsat = scmdata.ScmRun(magicc_output_gsat).filter(
        scenario=scenarios_to_run, year=run_years
    )

    # convert OHC to hfds in a crude way
    openscm_ohc = scmdata.ScmRun(magicc_output_ohc).filter(scenario=scenarios_to_run)
    # TODO: check whether this should be earth surface area or ocean surface area to be compatible with what MESMER has done
    earth_surface_area = 510.1 * 10 ** 6 * unit_registry("km^2")
    openscm_hfds = (
        openscm_ohc.delta_per_delta_time(out_var="Heat Uptake|Ocean")
        .convert_unit("W")
        .filter(year=run_years)
    ) / earth_surface_area

    result = _draw_realisations_from_mesmer_file_and_openscm_output(
        mesmer_bundle_file=mesmer_bundle_file,
        openscm_gsat=openscm_gsat,
        seeds={"IPSL-CM6A-LR": {"all": {"gv": 0, "lv": 1000000}}},
        openscm_hfds=openscm_hfds,
        n_realisations_per_scenario=30,
    )

    assert isinstance(result, xr.Dataset)
    assert set(result.data_vars) == {"tas"}
    assert set(result.dims) == {"realisation", "scenario", "z", "year"}

    assert set(result["scenario"].values) == set(
        openscm_gsat.get_unique_meta("scenario")
    )

    # make sure we can get onto a lat lon grid from what is saved
    result_reshaped = result.set_index(z=("lat", "lon")).unstack("z")
    assert set(result_reshaped.dims) == {
        "scenario",
        "realisation",
        "lon",
        "lat",
        "year",
    }


def test_create_realisations_from_pre_run_data_with_unrecognised_scenario_name(
    test_data_dir,
):
    mesmer_bundle_file = os.path.join(
        test_data_dir, "mesmer-bundles", "test-generic-mesmer-bundle.pkl"
    )

    magicc_output_dir = os.path.join(test_data_dir, "magicc-rcmip-phase-1-output")
    magicc_output_gsat = os.path.join(
        test_data_dir,
        magicc_output_dir,
        "rcmip-phase-1_magicc7.1.0.beta-canesm5-r1i1p1f1_world_surface-air-temperature-change.csv",
    )
    magicc_output_ohc = os.path.join(
        test_data_dir,
        magicc_output_dir,
        "rcmip-phase-1_magicc7.1.0.beta-canesm5-r1i1p1f1_world_heat-content-ocean.csv",
    )

    run_years = range(1850, 2150 + 1)
    scenarios_to_run = ["ssp126", "esm-ssp126"]

    openscm_gsat = scmdata.ScmRun(magicc_output_gsat).filter(
        scenario=scenarios_to_run, year=run_years
    )

    # convert OHC to hfds in a crude way
    openscm_ohc = scmdata.ScmRun(magicc_output_ohc).filter(scenario=scenarios_to_run)
    # TODO: check whether this should be earth surface area or ocean surface area to be compatible with what MESMER has done
    earth_surface_area = 510.1 * 10 ** 6 * unit_registry("km^2")
    openscm_hfds = (
        openscm_ohc.delta_per_delta_time(out_var="Heat Uptake|Ocean")
        .convert_unit("W")
        .filter(year=run_years)
    ) / earth_surface_area

    result = _draw_realisations_from_mesmer_file_and_openscm_output(
        mesmer_bundle_file=mesmer_bundle_file,
        openscm_gsat=openscm_gsat,
        seeds={"IPSL-CM6A-LR": {"all": {"gv": 0, "lv": 1000000}}},
        openscm_hfds=openscm_hfds,
        n_realisations_per_scenario=30,
    )

    assert isinstance(result, xr.Dataset)
    assert set(result.data_vars) == {"tas"}
    assert set(result.dims) == {"realisation", "scenario", "z", "year"}

    assert set(result["scenario"].values) == set(
        openscm_gsat.get_unique_meta("scenario")
    )

    # make sure we can get onto a lat lon grid from what is saved
    result_reshaped = result.set_index(z=("lat", "lon")).unstack("z")
    assert set(result_reshaped.dims) == {
        "scenario",
        "realisation",
        "lon",
        "lat",
        "year",
    }
