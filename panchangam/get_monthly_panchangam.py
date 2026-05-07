from datetime import datetime
from typing import Dict
import calendar

from panchangam.astronomical_calculations import get_panchangam


cal = calendar.Calendar()

def get_monthly_panchangam(
        year: int, 
        month: int, 
        latitude_degrees: float,
        longitude_degrees: float,
        timezone: str
    )-> Dict:
    data = {}
    for day in cal.itermonthdates(year, month):
        panchangam = {}
        if day.month == month:
            localdt = datetime(
                year=day.year,
                month=day.month,
                day=day.day,
                hour=0,
                minute=0,
                second=0
            )
            panchangam = get_panchangam(
                localdt=localdt,
                latitude_degrees=latitude_degrees,
                longitude_degrees=longitude_degrees,
                timezone=timezone
            )
            data[day.isoformat()] = panchangam
    return data


