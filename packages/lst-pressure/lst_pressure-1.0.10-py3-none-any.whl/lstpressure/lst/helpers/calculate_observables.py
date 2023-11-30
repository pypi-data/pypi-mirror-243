from functools import lru_cache
from datetime import datetime
from ...observable import Observable
from ...observation import Observation
from ...lstcalendar import LSTCalendar
from perf import track_total_runtime


@track_total_runtime
@lru_cache(maxsize=None)
def calculate_observables(
    cal_start: str | datetime,
    cal_end: str | datetime,
    observations: list[Observation],
    latitude: str | float,
    longitude: str | float,
) -> list[Observable]:
    return sorted(
        LSTCalendar(
            cal_start, cal_end, observations=observations, latitude=latitude, longitude=longitude
        ).observables()
    )
