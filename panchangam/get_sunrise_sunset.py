from typing import Tuple, Optional, Union
from skyfield.api import load, Topos
from skyfield import almanac
from datetime import date, datetime
import pytz

# Load ephemeris data
ts = load.timescale()
ephem = load('de421.bsp')

def get_sunrise_sunset(date: date, location: Topos, timezone: str) -> Tuple[datetime, datetime]:
    """
    Calculate sunrise and sunset times for a given date, location, and timezone.

    Args:
        date (date): The date for which to calculate sunrise/sunset.
        location (Topos): The location (latitude, longitude) for calculations.
        timezone (str): The timezone (e.g., 'Asia/Kolkata') for local time conversion.

    Returns:
        Tuple[datetime, datetime]: (sunrise_local, sunset_local) in the specified timezone.

    Raises:
        ValueError: If sunrise or sunset times are unavailable.
    """
    # Define the time range for the day (UTC)
    t0 = ts.utc(date.year, date.month, date.day)
    t1 = ts.utc(date.year, date.month, date.day + 1)

    # Find sunrise and sunset times (UTC)
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(ephem, location))

    # Convert to local timezone
    tz = pytz.timezone(timezone)
    sunrise_local: Optional[datetime] = None
    sunset_local: Optional[datetime] = None

    for time_utc, is_rising in zip(t, y):
        # Convert skyfield Time to Python datetime (UTC)
        utc_dt: datetime = time_utc.utc_datetime()

        local_dt = utc_dt.astimezone(tz)

        if is_rising:
            sunrise_local = local_dt
        else:
            sunset_local = local_dt

    if sunrise_local is not None and sunset_local is not None:
        return sunrise_local, sunset_local

    raise ValueError("Sunrise and sunset times unavailable for the given date and location.")
