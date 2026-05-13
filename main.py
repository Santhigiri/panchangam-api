from kollavarsham import Kollavarsham
import uvicorn
import os
import logging
from datetime import date, datetime
from typing import Annotated
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
from pydantic.main import BaseModel
from panchangam.astronomical_calculations import get_panchangam
from panchangam.constants import DEFAULT_TIMEZONE, Coordinates
from panchangam.get_monthly_panchangam import get_kollavarasham, get_monthly_panchangam


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
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
    kv: Kollavarsham = Depends(get_kollavarasham)
):

    try:
        date = datetime.strptime(str(params.date_str), "%Y-%m-%d")
        time = datetime.strptime(params.time_str, "%H:%M:%S").time()
        localdt = datetime.combine(date, time)
    except ValueError:
        return {'error': 'Invalid Date format. Use YYYY-MM-DD'}, 400


    return get_panchangam(
        kv=kv,
        localdt=localdt,
        latitude_degrees=params.latitude,
        longitude_degrees=params.longitude,
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
    kv: Kollavarsham = Depends(get_kollavarasham)
):
    return get_monthly_panchangam(
        kv=kv,
        year=params.year,
        month=params.month,
        latitude_degrees=params.latitude,
        longitude_degrees=params.longitude,
        timezone=params.timezone
    )



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT",8000)), log_level="info")
