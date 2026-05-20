from typing import Annotated
from fastapi import APIRouter, Query
from datetime import datetime

from pytz import timezone
from core.astronomy.sunrise_sunset import get_sunrise_sunset
from core.calendar.monthly_panchangam import get_monthly_panchangam
from core.calendar.panchangam import get_panchangam
from schemas.GetMonthlyPanchangamParams import GetMonthlyPanchangamParams
from schemas.GetDayPanchangamParams import GetPanchangamParams


router = APIRouter(prefix='/panchangam')

@router.get('/')
def panchangam(
    params: Annotated[GetPanchangamParams, Query()],
):
    try:
        date = datetime.strptime(str(params.date_str), "%Y-%m-%d")
        time = datetime.strptime(params.time_str, "%H:%M:%S").time()
        latitude_degrees = round(params.latitude,3)
        longitude_degrees = round(params.longitude,3)
        localdt = datetime.combine(date, time)
        sunrise_dt, sunset_dt = get_sunrise_sunset(
            date=date.date(),
            latitude=latitude_degrees,
            longitude=longitude_degrees,
            timezone=params.timezone
        )
    except ValueError:
        return {'error': 'Invalid Date format. Use YYYY-MM-DD'}, 400



    return get_panchangam(
        localdt=localdt,
        sunrise_dt=sunrise_dt,
        sunset_dt =sunset_dt, 
        latitude=latitude_degrees,
        longitude=longitude_degrees,
        timezone=params.timezone
    )


@router.get('/monthly')
def panchangam_monthly(
    params: Annotated[GetMonthlyPanchangamParams, Query()],
):
    return get_monthly_panchangam(
        year=params.year,
        month=params.month,
        latitude_degrees=round(params.latitude,3),
        longitude_degrees=round(params.longitude,3),
        timezone=params.timezone
    )
