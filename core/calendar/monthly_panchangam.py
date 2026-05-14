from typing import Any, Dict
import calendar
from core.astronomy.sunrise_sunset import get_sunrise_sunset
from core.calendar.panchangam import get_panchangam

cal = calendar.Calendar(firstweekday=6)

def get_monthly_panchangam(
        year: int, 
        month: int, 
        latitude_degrees: float,
        longitude_degrees: float,
        timezone: str,
    )-> Dict[str,Any]:
    data = {}
    for day in cal.itermonthdates(year, month):
        panchangam = {}
        sunrise_dt, sunset_dt = get_sunrise_sunset(
                date =day,
        )
        localdt = sunrise_dt.replace(tzinfo=None)
        panchangam = get_panchangam(
            localdt=localdt,
            sunrise_dt=sunrise_dt,
            sunset_dt = sunset_dt,
            latitude=latitude_degrees,
            longitude=longitude_degrees,
            timezone=timezone
        )
        data[day.isoformat()] = panchangam
    print(get_sunrise_sunset.cache_info())
    return data
