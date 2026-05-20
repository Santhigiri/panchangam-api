from datetime import datetime
from typing import Any, Dict
import pytz
from core.astronomy.calculations import get_sun_sidereal_longitude
from core.astronomy.nakshatra import get_nakshatra
from core.astronomy.nakshatra_transition import calc_nakshatra_transition
from core.astronomy.thithi import get_thithi
from core.astronomy.pournami import is_poornima
from core.astronomy.thithi_transition import calc_thithi_transition, get_thithi_transition
from core.calendar.kollavarsham import get_kollavarsham_date


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
    sun_sidereal_longitude = get_sun_sidereal_longitude(localdt=localdt, timezone=timezone)

    thithi_transition = calc_thithi_transition(localdt.date(), timezone=timezone)

    nakshatra_transition = calc_nakshatra_transition(localdt.date(),timezone)

    is_pournami: bool = is_poornima(localdt=localdt, timezone=timezone)
    kv_day = get_kollavarsham_date(dt=localdt.date(), latitude=latitude, longitude=longitude, timezone=timezone)

    return {
        "date": localdt.astimezone(tz=pytz.timezone(timezone)),
        "calculated_ml_day": kv_day['malayalam_day'],
        "calculated_ml_month": kv_day['malayalam_month'],
        "calculated_ml_year": kv_day['kollam_year'],
        "nakshatra": nakshatra,
        "nakshatra_transitions": nakshatra_transition,
        "thithi": thithi,
        "thithi_transitions": thithi_transition,
        "sunrise": sunrise_dt.time().isoformat(timespec="minutes"),
        "sunset": sunset_dt.time().isoformat(timespec="minutes"),
        "is_pournami": is_pournami,
        "sun_sidereal_longitude": sun_sidereal_longitude,
        "moon_sidereal_longitude": moon_sidereal_longitude
    }
