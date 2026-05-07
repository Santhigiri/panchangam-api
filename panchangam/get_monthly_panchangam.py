from datetime import datetime
from typing import Dict
import calendar
from fastapi import Depends
import kollavarsham
from panchangam.astronomical_calculations import get_panchangam

def get_kollavarasham(latitude: float, longitude: float):
    return kollavarsham.Kollavarsham(latitude=latitude, longitude=longitude, system="SuryaSiddhanta")

cal = calendar.Calendar(firstweekday=6)

def get_monthly_panchangam(
        year: int, 
        month: int, 
        latitude_degrees: float,
        longitude_degrees: float,
        timezone: str,
        kv: kollavarsham.Kollavarsham = Depends(get_kollavarasham)
    )-> Dict:
    data = {}
    for day in cal.itermonthdates(year, month):
        panchangam = {}
        localdt = datetime(
            year=day.year,
            month=day.month,
            day=day.day,
            hour=0,
            minute=0,
            second=0
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



