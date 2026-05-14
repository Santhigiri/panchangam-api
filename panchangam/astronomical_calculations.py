from datetime import datetime
from functools import lru_cache
import math
from typing import Any, Tuple
import numpy as np
from numpy.typing import NDArray
import pytz
from pytz.exceptions import Error
from skyfield import api
from skyfield.api import Time, load, Topos
from skyfield.framelib import ecliptic_frame
from panchangam.constants import THITHI_NAMES, THITHI_NAMES_ML
from panchangam.get_ayanamsa import get_ayanamsa
from panchangam.utils import calc_nakshatra_from_lon
import pytz
import logging

ephem = load('de421.bsp')
earth = ephem['earth']
sun = ephem['sun']
moon = ephem['moon']
ts = api.load.timescale()


# 1. Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_time(localdt: datetime, timezone: str)-> Time: 
    # Date: May 7, 2026, 6:00 AM IST
    tz = pytz.timezone(timezone)
    local_time = tz.localize(localdt)
    utc_time = local_time.astimezone(pytz.UTC)
    t = ts.utc(utc_time.year, utc_time.month, utc_time.day,
            utc_time.hour, utc_time.minute, utc_time.second)
    return t


def get_tropical_longitude( t: Time, body: str) -> float:
    pos = None
    if body == 'moon':
        pos = earth.at(t).observe(moon).apparent().frame_latlon(ecliptic_frame)
    elif body == 'sun':
        pos = earth.at(t).observe(sun).apparent().frame_latlon(ecliptic_frame)
    else:
        raise Error("Invalid body. body should be 'moon' or 'sun'")
    tropical_longitude = float(pos[1].degrees) % 360
    return tropical_longitude


def get_sidereal_longitude(
    localdt: datetime,
    timezone: str,
    body: str) -> float:
    t = get_time(localdt, timezone)
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

def get_moon_sidereal_longitude(
    localdt: datetime,
    timezone: str
)-> float:
    return get_sidereal_longitude(localdt=localdt, timezone=timezone, body= "moon")

@lru_cache(maxsize=1000)
def get_sun_sidereal_longitude(
    localdt: datetime,
    timezone: str
    ):
    return get_sidereal_longitude(localdt=localdt, timezone=timezone, body= "sun")

def get_nakshatra(localdt: datetime, timezone: str)->Tuple[str, float]:
    # Calculate Moon's sidereal longitude
    moon_sidereal_longitude = get_moon_sidereal_longitude(localdt=localdt, timezone=timezone)

    # Determine Nakshatra using sidereal longitude
    nakshatra = calc_nakshatra_from_lon(moon_sidereal_longitude)

    return nakshatra, moon_sidereal_longitude

def get_thithi(
    localdt: datetime,
    timezone: str
)-> str:
    # Thithi calculation
    moon_sidereal_longitude = get_moon_sidereal_longitude(localdt, timezone)
    sun_sidereal_longitude = get_sun_sidereal_longitude(localdt, timezone)
    elongation = (moon_sidereal_longitude - sun_sidereal_longitude) % 360
    thithi_number = math.floor(elongation / 12) + 1
    if thithi_number > 30:
        thithi_number = 30  # Amavasya
    thithi_name = THITHI_NAMES[thithi_number - 1]
    return thithi_name



def is_poornima(localdt: datetime, timezone: str)-> bool:
    night_time = datetime(
        year=localdt.year,
        month=localdt.month,
        day=localdt.day,
        hour=23,
        minute=59,
        second=59
    )
    thithi = get_thithi(night_time, timezone)

    return thithi == "Pournami"

def get_localdtz(localdt: datetime, timezone: str):
    return pytz.timezone(timezone).localize(localdt)


