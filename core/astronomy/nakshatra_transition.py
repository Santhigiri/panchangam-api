
from datetime import date, datetime, timedelta
from functools import lru_cache
from typing import List
from zoneinfo import ZoneInfo

from numpy import ndarray
from skyfield.almanac import find_discrete
from skyfield.api import Time
from core.astronomy import nakshatra
from core.astronomy.calculations import get_time
from core.astronomy.ephemeris import ephem, ts

from core.astronomy.thithi_transition import get_sidereal_longitude_from_time
from core.constants import DEFAULT_TIMEZONE
from utils.utils import calc_nakshatra_from_lon


def get_nakshatra(t: Time):
    moon_sidereal_longitude = get_sidereal_longitude_from_time(t, "moon")
    nakshatra = calc_nakshatra_from_lon(moon_sidereal_longitude)
    return nakshatra

def get_nakshatra_transition(t: Time) -> bool:
    moon_sidereal_longitude = get_sidereal_longitude_from_time(t, "moon")
    return moon_sidereal_longitude % 13.33333 < 0.01

@lru_cache(maxsize=1000)
def calc_nakshatra_transition(date: date, timezone: str):
    t0 = ts.utc(date.year, date.month, date.day -1 , 0, 0, 0)
    t1 = ts.utc(date.year, date.month, date.day + 1 , 23, 59 , 59)

    get_nakshatra_transition.step_days = 0.0007

    t, values = find_discrete(t0, t1, get_nakshatra_transition)

    transition_times = [ti for ti, vi in zip(t, values) if vi == 1]


    nakshatras_for_day: List = []

    timezone_info = ZoneInfo(timezone)
    for i, ti in enumerate(transition_times):
        if i + 1 >= len(transition_times):
            break
        nakshatra_start_utc = ti.utc_datetime()
        nakshatra_start_tz: datetime = nakshatra_start_utc.astimezone(timezone_info)
        nakshatra_end_tz: datetime | None = None
        nakshatra = get_nakshatra(ts.from_datetime(nakshatra_start_utc) + timedelta(minutes=10))
        end_time = transition_times[i + 1]
        nakshatra_end_utc = end_time[0].utc_datetime() if isinstance(end_time, ndarray) else end_time.utc_datetime()
        nakshatra_end_tz = nakshatra_end_utc.astimezone(timezone_info)
        nakshatras_for_day.append({
            "nakshatra_name": nakshatra,
            "start_time": nakshatra_start_tz,
            "end_time": nakshatra_end_tz
        })
    
    return nakshatras_for_day
        

        
        


