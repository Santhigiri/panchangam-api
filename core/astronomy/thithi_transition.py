from datetime import date, datetime, timezone, timedelta
from functools import lru_cache
from typing import List
from pytz.exceptions import Error
from skyfield.almanac import ecliptic_frame, find_discrete
from skyfield.api import Time
from core.astronomy.ayanamsa import get_ayanamsa
from core.astronomy.ephemeris import ts
from zoneinfo import ZoneInfo
import numpy as np
import math
from core.constants import DEFAULT_TIMEZONE, THITHI_NAMES  # Python 3.9+
from core.astronomy.ephemeris import earth, sun, moon

def get_tropical_longitude( t: Time, body: str):
    pos = None
    if body == 'moon':
        pos = earth.at(t).observe(moon).apparent().frame_latlon(ecliptic_frame)
    elif body == 'sun':
        pos = earth.at(t).observe(sun).apparent().frame_latlon(ecliptic_frame)
    else:
        raise Error("Invalid body. body should be 'moon' or 'sun'")
    tropical_longitude = pos[1].degrees
    #print(f"TROPICAL LONGITUDE at {t.utc_datetime()}: {tropical_longitude}")
    
    return tropical_longitude


def get_sidereal_longitude_from_time(
    t: Time,
    body: str) -> float:
    tropical_longitude = get_tropical_longitude(
        t=t,
        body=body
    )
    dt = t.utc_datetime()
    year = dt[0].year if isinstance(dt, np.ndarray)  else dt.year
    month = dt[0].month if isinstance(dt, np.ndarray)  else dt.month
    day = dt[0].day if isinstance(dt, np.ndarray)  else dt.day
    hour = dt[0].hour if isinstance(dt, np.ndarray)  else dt.hour

    ayanamsa = get_ayanamsa(year = year, month =  month, day=day, hour=hour)
    
    return (tropical_longitude - ayanamsa) % 360


def get_elongations(t: Time) -> float:
    moon_sidereal_longitude = get_sidereal_longitude_from_time(t,"moon")
    sun_sidereal_longitude = get_sidereal_longitude_from_time(t, "sun")
    elongation = (moon_sidereal_longitude - sun_sidereal_longitude) % 360
    #print(f"ELONGATION AT {t.utc_datetime()}: {elongation}")
    return elongation


def get_thithi(
    t: Time
)-> str:
    # Thithi calculation
    elongation = get_elongations(t)
    thithi_number = math.floor(elongation / 12) + 1
    if thithi_number > 30:
        thithi_number = 30  # Amavasya
    thithi_name = THITHI_NAMES[thithi_number - 1]
    return thithi_name

def get_thithi_transition(t: Time) -> bool:
    elongation = get_elongations(t)
    return elongation % 12 < 0.01



@lru_cache(maxsize=1000)
def calc_thithi_transition(date: date, timezone: str):
    get_thithi_transition.step_days = 0.0007  # Step by 1 minute
    
    # Add the step_days attribute to the function

    t0 = ts.utc(date.year, date.month, date.day - 1, 0, 0, 0)
    t1 = ts.utc(date.year, date.month, date.day + 1,23,59,59)

    t, values = find_discrete(t0, t1, get_thithi_transition)

    # Filter to keep only the start of transitions (values == 1)
    transition_times = [ti for ti, vi in zip(t, values) if vi == 1]

    thithis_for_day: List = []

    # Convert UTC to IST (UTC+05:30)
    ist_timezone = ZoneInfo(timezone)
    for i, ti in enumerate(transition_times):
        utc_start_time = ti.utc_datetime()
        ist_start_time: datetime = utc_start_time.astimezone(ist_timezone)
        ist_end_time = None
        if i + 1 != len(transition_times):
            utc_end_time = transition_times[i+1].utc_datetime()
            ist_end_time = utc_end_time.astimezone(ist_timezone)
        thithi = get_thithi(ts.from_datetime(utc_start_time) + timedelta(minutes=10))
        if ist_end_time is not None:
            thithis_for_day.append({
                "thithi_name": thithi,
                "ist_start_time": ist_start_time,
                "ist_end_time": ist_end_time
            })
        #print(f"{thithi} {start_time_str} - {end_time_str} ")

    return thithis_for_day
