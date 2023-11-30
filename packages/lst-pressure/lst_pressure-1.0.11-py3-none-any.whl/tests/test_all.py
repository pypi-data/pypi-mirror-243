import pytest
from lstpressure.lstcalendar import LSTCalendar
from lstpressure.observation import Observation, is_observable
from lstpressure.lstindex import LSTIntervalType as I

# 20231030 LST dusk is about 2130

tests = [
    # (lst_window_start, lst_window_end, utc_constraints, duration, dt_range, observables_count)
    (8, 20, [I.NIGHT], 2, ["20231030"], 0),
    (8, 20, [], 2, ["20231030"], 2),
    (2, 20, [I.NIGHT], 0.5, ["20231030"], 1),
    (20, 1, [I.NIGHT], 2, ["20231030"], 2),
    (20, 1, [I.NIGHT], 2, ["20231030", "20231031"], 4),
    (20, 1, [], 2, ["20231030", "20231031"], 10),
    (20, 1, [], 2, ["20231106"], 5),
    (20, 1, [I.SUNRISE_SUNSET], 2, ["20231030", "20231031"], 0),
    (20, 1, [I.SUNSET_SUNRISE], 2, ["20231030", "20231031"], 4),
    (12.5, 15.5, None, None, ["20231107"], 2),  # FROM OPT
]


@pytest.mark.parametrize(
    "lst_window_start, lst_window_end, utc_constraints, duration, dt_range, observables_count",
    tests,
)
def test_is_observable(
    lst_window_start,
    lst_window_end,
    utc_constraints,
    duration,
    dt_range,
    observables_count,
):
    assert is_observable(
        Observation("~", lst_window_start, lst_window_end, utc_constraints, duration), *dt_range
    ) is bool(observables_count)


@pytest.mark.parametrize(
    "lst_window_start, lst_window_end, utc_constraints, duration, dt_range, observables_count",
    tests,
)
def test_observation_observables(
    lst_window_start,
    lst_window_end,
    utc_constraints,
    duration,
    dt_range,
    observables_count,
):
    assert (
        len(
            sorted(
                Observation(
                    "~", lst_window_start, lst_window_end, utc_constraints, duration
                ).observables(lstcalendar=LSTCalendar(*dt_range))
            )
        )
        == observables_count
    )


@pytest.mark.parametrize(
    "lst_window_start, lst_window_end, utc_constraints, duration, dt_range, observables_count",
    tests,
)
def test_calendar_observables(
    lst_window_start,
    lst_window_end,
    utc_constraints,
    duration,
    dt_range,
    observables_count,
):
    assert (
        len(
            sorted(
                LSTCalendar(*dt_range).observables(
                    [Observation("~", lst_window_start, lst_window_end, utc_constraints, duration)]
                )
            )
        )
        == observables_count
    )
