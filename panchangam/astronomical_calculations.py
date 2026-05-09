from datetime import datetime
import math
import numpy as np
from typing import Any, Dict, Union
from numpy.typing import NDArray
import pytz
from skyfield import api
from skyfield.api import Time, load, Topos
from skyfield.data import mpc
from skyfield.framelib import ecliptic_frame
from skyfield.positionlib import Geocentric
from panchangam.constants import NAKSHATRA_BOUNDARIES, NAKSHATRA_NAMES, THITHI_NAMES
from panchangam.get_ayanamsa import get_ayanamsa
from panchangam.get_sunrise_sunset import get_sunrise_sunset
from panchangam.utils import calc_nakshatra_from_lon
import pytz
import kollavarsham
import logging

celestial_bodies = load('de421.bsp')
earth = celestial_bodies['earth']
sun = celestial_bodies['sun']
moon = celestial_bodies['moon']
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
    logger.info(f"${local_time}")
    utc_time = local_time.astimezone(pytz.UTC)
    t = ts.utc(utc_time.year, utc_time.month, utc_time.day,
            utc_time.hour, utc_time.minute, utc_time.second)
    return t


def get_tropical_longitude( t: Time, body: NDArray[Any]) -> float:
    pos = earth.at(t).observe(body).apparent().frame_latlon(ecliptic_frame)
    tropical_longitude = float(pos[1].degrees) % 360
    return tropical_longitude


def get_sidereal_longitude(location: Topos, t: Time, body: NDArray[Any]) -> float:
    tropical_longitude = get_tropical_longitude(
        t=t,
        body=body
    )
    dt = t.utc_datetime()
    year = dt[0].year if isinstance(dt, np.ndarray)  else dt.year
    month = dt[0].month if isinstance(dt, np.ndarray)  else dt.month
    day = dt[0].day if isinstance(dt, np.ndarray)  else dt.day
    logger.info(f"TROPICAL LONGITUDE: {tropical_longitude}")
    ayanamsa = get_ayanamsa(year = year, month =  month, day=day)
    
    return (tropical_longitude - ayanamsa) % 360

def get_moon_sidereal_longitude(location: Topos, t: Time)-> float:
    return get_sidereal_longitude(location=location, t=t, body= moon)

def get_sun_sidereal_longitude(location: Topos, t: Time):
    return get_sidereal_longitude(location=location, t=t, body= sun)


def get_nakshatra(location: Topos, t: Time)->str:
    # Calculate Moon's sidereal longitude
    moon_sidereal_longitude = get_sidereal_longitude(location=location, t=t,body=moon)
    logger.info(f"MOON'S SIDEREAL LONGITUDE: {moon_sidereal_longitude}")

    # Determine Nakshatra using sidereal longitude
    nakshatra = calc_nakshatra_from_lon(moon_sidereal_longitude)

    return nakshatra

def get_thithi(location: Topos, t: Time)-> str:
    # Thithi calculation
    moon_sidereal_longitude = get_sidereal_longitude(location=location, t=t, body=moon)
    sun_sidereal_longitude = get_sidereal_longitude(location=location, t=t, body=sun)
    elongation = (moon_sidereal_longitude - sun_sidereal_longitude) % 360
    thithi_number = math.floor(elongation / 12) + 1
    if thithi_number > 30:
        thithi_number = 30  # Amavasya
    thithi_name = THITHI_NAMES[thithi_number - 1]
    return thithi_name


def get_kollavarsham_details(
    kv: kollavarsham.Kollavarsham,
    localdt: datetime,
    timezone: str
)-> kollavarsham.KollavarshamDate:

    tz = pytz.timezone(timezone)
    localdtz = tz.localize(localdt)

    kv_date = kv.from_gregorian_date(date=localdtz)

    return kv_date



def is_poornima(localdt: datetime,location: Topos, timezone: str)-> bool:
    night_time = datetime(
        year=localdt.year,
        month=localdt.month,
        day=localdt.day,
        hour=23,
        minute=59,
        second=59
    )
    t: Time = get_time(night_time,timezone=timezone)
    thithi = get_thithi(location=location, t=t)

    return thithi == "Pournami"

def get_localdtz(localdt: datetime, timezone: str):
    return pytz.timezone(timezone).localize(localdt)


def get_panchangam(
    kv: kollavarsham.Kollavarsham,
    localdt: datetime,
    latitude_degrees: float,
    longitude_degrees: float,
    timezone: str = 'Asia/Kolkata'
    )->Dict[str,Any]:
    #TODO: calculate and return all values as json
    location = Topos(latitude_degrees=latitude_degrees, longitude_degrees=longitude_degrees)
    t: Time = get_time(localdt=localdt, timezone=timezone)
    nakshatra: str = get_nakshatra(location=location,t=t)
    thithi: str = get_thithi(location=location, t=t)

    sunrise_local, sunset_local = get_sunrise_sunset(localdt.date(), location=location, timezone=timezone)
    moon_sidereal_longitude = get_sidereal_longitude(location=location, t=t,body=moon)

    kv_date  = get_kollavarsham_details(
        kv=kv,
        localdt=localdt,
        timezone=timezone
    )

    is_pournami: bool = is_poornima(localdt=localdt,location=location, timezone=timezone)

    return {
        "date": localdt.astimezone(tz=pytz.timezone(timezone)),
        "malayalam_year": f"{kv_date.year}",
        "malayalam_month": f"{kv_date.masa_name.strip()}",
        "malayalam_day": f"{kv_date.date}",
        "kollavarsham_nakshatra": f"{kv_date.ml_naksatra_name}",
        "nakshatra": nakshatra,
        "thithi": thithi,
        "sunrise": sunrise_local.time().isoformat(timespec="minutes"),
        "sunset": sunset_local.time().isoformat(timespec="minutes"),
        "is_pournami": is_pournami,
        "moon_sidereal_longitude": moon_sidereal_longitude
    }
