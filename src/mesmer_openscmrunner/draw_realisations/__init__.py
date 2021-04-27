import joblib

import mesmer.create_emulations
import xarray as xr


def _draw_realisations_from_mesmer_file_and_openscm_output(
    mesmer_bundle_file,
    openscm_gsat,
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
    time_mesmer = mesmer_bundle["time"]

    gsat_scenarios = set(openscm_gsat.get_unique_meta("scenario"))
    hfds_scenarios = set(openscm_hfds.get_unique_meta("scenario"))
    if gsat_scenarios != hfds_scenarios:
        raise ValueError("gsat_scenarios: {}, hfds_scenarios: {}".format(gsat_scenarios, hfds_scenarios))

    openscm_gsat_for_mesmer = _prepare_openscm_gsat(openscm_gsat)
    openscm_hfds_for_mesmer = _prepare_openscm_hfds(openscm_hfds)

    out = []
    for scen_gsat in openscm_gsat_for_mesmer.groupby("scenario"):
        scenario = scen_gsat.get_unique_meta("scenario", True)
        if scenario not in mesmer_bundle["time"]:
            raise ValueError("No MESMER calibration available for: {}".format(scenario))

        hist_tas = _filter_and_assert_1d(
            scen_gsat.filter(year=time_mesmer["hist"])
        )
        scen_tas = _filter_and_assert_1d(
            scen_gsat.filter(year=time_mesmer[scenario])
        )

        scen_hfds = openscm_hfds_for_mesmer.filter(scenario=scenario)
        hist_hfds = _filter_and_assert_1d(
            scen_hfds.filter(year=time_mesmer["hist"])
        )
        scen_hfds = _filter_and_assert_1d(
            scen_hfds.filter(year=time_mesmer[scenario])
        )

        preds_lt_scenario = {
            "gttas": {"hist": hist_tas, scenario: scen_tas},
            "gttas2": {"hist": hist_tas ** 2, scenario: scen_tas ** 2},
            "gthfds": {"hist": hist_hfds, scenario: scen_hfds},
        }

        result_scenario = mesmer.create_emulations.make_realisations(
            preds_lt_scenario,
            mesmer_bundle["params_lt"],
            mesmer_bundle["params_lv"],
            mesmer_bundle["params_gv_T"],
            n_realisations=n_realisations_per_scenario,
            seeds=mesmer_bundle["seeds"],
            land_fractions=mesmer_bundle["land_fractions"],
            time=time_mesmer,
        )
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
        raise ValueError("Filters gave non-1D data: {}, {}".format(filtered.shape, kwargs))

    return filtered
