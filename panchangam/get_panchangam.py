from datetime import datetime
from typing import Any, Dict
import pytz
from skyfield.api import Time, Topos

from panchangam.astronomical_calculations import get_moon_sidereal_longitude, get_nakshatra, get_sidereal_longitude, get_thithi, get_time, is_poornima
from panchangam.get_kollavarsham import get_kollavarsham_date


def get_panchangam(
    localdt: datetime,
    sunrise_dt: datetime,
    sunset_dt: datetime,
    latitude: float,
    longitude: float,
    timezone: str = 'Asia/Kolkata'
    )->Dict[str,Any]:
    #TODO: calculate and return all values as json
    nakshatra, moon_sidereal_longitude = get_nakshatra(localdt= localdt,timezone=timezone)
    thithi: str = get_thithi(localdt=localdt, timezone=timezone)


    is_pournami: bool = is_poornima(localdt=localdt, timezone=timezone)
    kv_day = get_kollavarsham_date(dt=localdt.date(), latitude=latitude, longitude=longitude, timezone=timezone)

    return {
        "date": localdt.astimezone(tz=pytz.timezone(timezone)),
        "calculated_ml_day": kv_day['malayalam_day'],
        "calculated_ml_month": kv_day['malayalam_month'],
        "calculated_ml_year": kv_day['kollam_year'],
        "nakshatra": nakshatra,
        "thithi": thithi,
        "sunrise": sunrise_dt.time().isoformat(timespec="minutes"),
        "sunset": sunset_dt.time().isoformat(timespec="minutes"),
        "is_pournami": is_pournami,
        "moon_sidereal_longitude": moon_sidereal_longitude
    }
