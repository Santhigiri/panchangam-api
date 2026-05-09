from datetime import date, datetime
from typing import Dict
import calendar
from fastapi import Query
import kollavarsham
from skyfield.api import Topos
from panchangam.astronomical_calculations import get_panchangam
from panchangam.get_sunrise_sunset import get_sunrise_sunset

def get_kollavarasham(latitude: float = Query(), longitude: float = Query()):
    return kollavarsham.Kollavarsham(latitude=latitude, longitude=longitude, system="SuryaSiddhanta")

cal = calendar.Calendar(firstweekday=6)

def get_monthly_panchangam(
        year: int, 
        month: int, 
        latitude_degrees: float,
        longitude_degrees: float,
        timezone: str,
        kv: kollavarsham.Kollavarsham
    )-> Dict:
    data = {}
    for day in cal.itermonthdates(year, month):
        panchangam = {}
        sunrise_dt, _ = get_sunrise_sunset(
                date =day,
                location= Topos(latitude_degrees=latitude_degrees, longitude_degrees = longitude_degrees),
                timezone=timezone
        )
        localdt = datetime(
            year=day.year,
            month=day.month,
            day=day.day,
            hour=sunrise_dt.hour,
            minute=sunrise_dt.minute,
            second=sunrise_dt.second
        )
        panchangam = get_panchangam(
            kv=kv,
            localdt=localdt,
            latitude_degrees=latitude_degrees,
            longitude_degrees=longitude_degrees,
            timezone=timezone
        )
        data[day.isoformat()] = panchangam
    return data



