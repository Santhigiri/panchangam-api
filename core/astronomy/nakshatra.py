from datetime import datetime
from typing import Tuple
from core.astronomy.calculations import get_moon_sidereal_longitude
from utils.utils import calc_nakshatra_from_lon

def get_nakshatra(localdt: datetime, timezone: str)->Tuple[str, float]:
    # Calculate Moon's sidereal longitude
    moon_sidereal_longitude = get_moon_sidereal_longitude(localdt=localdt, timezone=timezone)

    # Determine Nakshatra using sidereal longitude
    nakshatra = calc_nakshatra_from_lon(moon_sidereal_longitude)

    return nakshatra, moon_sidereal_longitude
