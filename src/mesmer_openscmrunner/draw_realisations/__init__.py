# MESMER-OpenSCM Runner, land-climate dynamics group, S.I. Seneviratne
# Copyright (c) 2021-2022 MESMER-OpenSCM Runner contributors, listed in AUTHORS, and ETH Zurich.
# Licensed under the GNU General Public License v3.0 or later; see LICENSE or https://www.gnu.org/licenses/


import joblib
import mesmer.create_emulations
import xarray as xr


def _draw_realisations_from_mesmer_file_and_openscm_output(
    mesmer_bundle_file,
    openscm_gsat,
    seeds,
    openscm_hfds=None,
    n_realisations_per_scenario=5,
):
    """
    Parameters
    ----------
    mesmer_bundle_file : str
        File in which the MESMER bundle is saved

    openscm_gsat : :obj:`scmdata.ScmRun`
        Global-mean surface air temperature change output to be used to drive MESMER's emulations

    seeds : dict
        - ["esm"] (dict):
            ["scenario"] (dict):
                ["gv"] (seed for global variability)
                ["lv"] (seed for local variability)

    openscm_hfds : [None, :obj:`scmdata.ScmRun`]
        If supplied, global-mean ocean heat uptake output to be used to drive MESMER's emulations

    n_realisations_per_scenario : int
        Number of realisations to draw for each scenario in ``openscm_gsat`` (and ``openscm_hfds`` if supplied)

    Returns
    -------
    :obj:`xr.Dataset`
        Emulations for each scenario

    Raises
    ------
    ValueError
        The scenarios in `openscm_gsat`` and ``openscm_hfds`` (if supplied) aren't the same

    ValueError
        [TODO talk to Lea about what to do here] The scenarios in ``openscm_gsat`` don't match those for which MESMER has been calibrated

    ValueError
        [TODO talk to Lea about what to do here] The scenarios in ``openscm_gsat`` span a longer time than MESMER has been calibrated for

    ValueError
        ``openscm_gsat`` contains variables other than ``"Surface Air Temperature Change"``

    ValueError
        ``openscm_hfds`` contains variables other than ``"Heat Uptake|Ocean"``
    """
    mesmer_bundle = joblib.load(mesmer_bundle_file)

    gsat_scenarios = set(openscm_gsat.get_unique_meta("scenario"))
    hfds_scenarios = set(openscm_hfds.get_unique_meta("scenario"))
    if gsat_scenarios != hfds_scenarios:
        raise ValueError(
            "gsat_scenarios: {}, hfds_scenarios: {}".format(
                gsat_scenarios, hfds_scenarios
            )
        )

    openscm_gsat_for_mesmer = _prepare_openscm_gsat(openscm_gsat)
    openscm_hfds_for_mesmer = _prepare_openscm_hfds(openscm_hfds)

    hard_coded_hist_years = range(1850, 2014 + 1)
    hard_coded_scen_years = range(2015, 3000 + 1)

    out = []
    for scen_gsat in openscm_gsat_for_mesmer.groupby("scenario"):
        scenario = scen_gsat.get_unique_meta("scenario", True)
        # if scenario not in mesmer_bundle["time"]:
        #     raise KeyError("No MESMER calibration available for: {}".format(scenario))

        hist_tas = _filter_and_assert_1d(scen_gsat.filter(year=hard_coded_hist_years))
        scen_tas = _filter_and_assert_1d(scen_gsat.filter(year=hard_coded_scen_years))

        openscm_hfds_for_mesmer_scen = openscm_hfds_for_mesmer.filter(scenario=scenario)
        hist_hfds = _filter_and_assert_1d(
            openscm_hfds_for_mesmer_scen.filter(year=hard_coded_hist_years)
        )
        scen_hfds = _filter_and_assert_1d(
            openscm_hfds_for_mesmer_scen.filter(year=hard_coded_scen_years)
        )

        # TODO: remove hard-coding and actually map up with what MESMER expects
        preds_lt_scenario = {}
        for predictor in mesmer_bundle["params_lt"]["preds"]:
            if predictor == "gttas":
                hist_vals = hist_tas
                scen_vals = scen_tas
            elif predictor == "gttas2":
                hist_vals = hist_tas ** 2
                scen_vals = scen_tas ** 2
            elif predictor == "gthfds":
                hist_vals = hist_hfds
                scen_vals = scen_hfds

            preds_lt_scenario[predictor] = {"hist": hist_vals, scenario: scen_vals}

        result_scenario = mesmer.create_emulations.make_realisations(
            preds_lt=preds_lt_scenario,
            params_lt=mesmer_bundle["params_lt"],
            params_lv=mesmer_bundle["params_lv"],
            params_gv_T=mesmer_bundle["params_gv"],
            n_realisations=n_realisations_per_scenario,
            seeds=seeds,
            land_fractions=mesmer_bundle["land_fractions"],
            time={
                "hist": scen_gsat.filter(year=hard_coded_hist_years)["year"].values,
                scenario: scen_gsat.filter(year=hard_coded_scen_years)["year"].values,
            },
        )

        result_scenario = result_scenario.squeeze(
            dim="scenario", drop=True
        ).expand_dims({"scenario": [scenario]})
        out.append(result_scenario)

    out = xr.merge(out)

    return out


def _prepare_openscm_gsat(openscm_gsat):
    return openscm_gsat.convert_unit("K")


def _prepare_openscm_hfds(openscm_hfds):
    return openscm_hfds.convert_unit("W/m^2")


def _filter_and_assert_1d(scmrun, **kwargs):
    filtered = scmrun.filter(**kwargs).values.squeeze()
    if len(filtered.shape) != 1:
        raise ValueError(
            "Filters gave non-1D data: {}, {}".format(filtered.shape, kwargs)
        )

    return filtered
