from pydantic import Field, BaseModel
from core.constants import Coordinates, DEFAULT_TIMEZONE


class GetMonthlyPanchangamParams(BaseModel):
    year: int = Field(ge=1900, le=2100)
    month: int =  Field(ge=1,le=12)
    latitude: float = Coordinates.SG_LATITUDE
    longitude: float = Coordinates.SG_LONGITUDE
    timezone: str = DEFAULT_TIMEZONE
