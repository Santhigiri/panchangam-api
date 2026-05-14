from datetime import date, datetime
from typing import Annotated
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
from pydantic.main import BaseModel
from pytz import timezone
from skyfield.api import Topos
from panchangam.get_sunrise_sunset import get_sunrise_sunset
from panchangam.get_panchangam import get_panchangam
from panchangam.constants import DEFAULT_TIMEZONE, Coordinates
from panchangam.get_monthly_panchangam import  get_monthly_panchangam


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GetPanchangamParams(BaseModel):
    date_str: date = datetime.now().date()
    time_str: str = "00:00:00"
    latitude: float = Coordinates.SG_LATITUDE
    longitude: float = Coordinates.SG_LONGITUDE
    timezone: str = DEFAULT_TIMEZONE


@app.get('/panchangam')
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

class GetMonthlyPanchangamParams(BaseModel):
    year: int = Field(ge=1900, le=2100)
    month: int =  Field(ge=1,le=12)
    latitude: float = Coordinates.SG_LATITUDE
    longitude: float = Coordinates.SG_LONGITUDE
    timezone: str = DEFAULT_TIMEZONE

@app.get('/panchangam/monthly')
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
print(id(get_sunrise_sunset))
