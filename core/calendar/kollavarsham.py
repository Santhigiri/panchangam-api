from datetime import date, timedelta
from functools import lru_cache
from typing import Dict, Any

from pydantic import BaseModel

from core.astronomy.calculations import (
    get_sun_sidereal_longitude,
)

from core.constants import (
    DEFAULT_TIMEZONE,
    MALAYALAM_MONTH_ML,
)

from core.astronomy.sunrise_sunset import get_sunrise_sunset
from utils.malayalam_masa import MalayalamMasa

MALAYALAM_MONTHS = [
    "Medam",
    "Edavam",
    "Mithunam",
    "Karkidakam",
    "Chingam",
    "Kanni",
    "Thulam",
    "Vrischikam",
    "Dhanu",
    "Makaram",
    "Kumbham",
    "Meenam"
]

class KollavarshamDate(BaseModel):
    date: date
    kv_day: int
    kv_month: int
    kv_year: int
    kv_month_name_en: str
    kv_month_name_ml: str


def get_raasi(longitude: float) -> int:
    """
    Convert sidereal longitude to raasi index.
    """
    EPSILON = 1e-6
    normalized = (longitude - EPSILON) % 360
    return int(normalized // 30)


@lru_cache(maxsize=1000)
def get_sunset_raasi(
    dt: date,
    latitude: float,
    longitude: float,
    timezone: str = DEFAULT_TIMEZONE
) -> int:
    """
    Get Sun's raasi at local sunset.
    """

    _, sunset = get_sunrise_sunset(
        date=dt,
    )


    longitude = get_sun_sidereal_longitude(
        localdt=sunset.replace(tzinfo=None),
        timezone=timezone
    )

    return get_raasi(longitude)


@lru_cache(maxsize=1000)
def get_kollavarsham_date(
    dt: date,
    latitude: float,
    longitude: float,
    timezone: str = DEFAULT_TIMEZONE
) -> KollavarshamDate:


    # Today's raasi at sunrise
    today_raasi = get_sunset_raasi(
        dt=dt,
        timezone=timezone,
        latitude=latitude,
        longitude=longitude
    )

    current_date = dt

    malayalam_day = 1

    # Walk backwards sunset-by-sunset
    while True:

        previous_date: date = current_date - timedelta(days=1)
        previous_raasi = get_sunset_raasi(
            dt=previous_date,
            latitude= latitude,
            longitude=longitude,
            timezone=timezone
        )

        # Month boundary found
        if previous_raasi != today_raasi:
            break

        malayalam_day += 1
        current_date = previous_date


    # Kollam Era year starts at Chingam
    if today_raasi >= 4:
        kollam_year = dt.year - 824
    else:
        kollam_year = dt.year - 825

    malayalam_masa = MalayalamMasa.from_id(today_raasi + 1)

    # Current solar longitude
    return KollavarshamDate(
        date= dt,
        kv_year= kollam_year,
        kv_month= malayalam_masa.id,
        kv_day= malayalam_day,
        kv_month_name_en=malayalam_masa.en,
        kv_month_name_ml=malayalam_masa.ml
    )

