from skyfield.api import load, Topos
from skyfield.framelib import ecliptic_frame
from datetime import date, datetime, timezone
import pytz
from panchangam.constants import NAKSHATRA_BOUNDARIES, NAKSHATRA_NAMES

# Load ephemeris
planets = load('de421.bsp')
earth = planets['earth']
sun = planets['sun']
moon = planets['moon']
ts = load.timescale()



def get_nakshatra(datetime: datetime, location: Topos, timezone: str = 'Asia/Kolkata'):

    # Kerala location (Thiruvananthapuram)
    position = earth + location

    # Date: May 7, 2026, 6:00 AM IST (sunrise)
    tz = pytz.timezone('Asia/Kolkata')
    local_time = tz.localize(datetime)
    t = ts.utc(local_time.year, local_time.month, local_time.day,
            local_time.hour, local_time.minute, local_time.second)

    # Calculate Moon's tropical longitude
    moon_pos = position.at(t).observe(moon).apparent().frame_latlon(ecliptic_frame)
    moon_tropical_longitude = float(moon_pos[1].degrees) % 360

    # Ayanamsa for 2026 (Lahiri)
    ayanamsa = 23.85  # 23°51' in decimal degrees TODO: implement a get_ayanamsa function

    # Calculate Moon's sidereal longitude
    moon_sidereal_longitude = (moon_tropical_longitude - ayanamsa) % 360

    # Determine Nakshatra using sidereal longitude
    for i, boundary in enumerate(NAKSHATRA_BOUNDARIES):
        if moon_sidereal_longitude < boundary:
            nakshatra = NAKSHATRA_NAMES[i]
            break
    else:
        nakshatra = NAKSHATRA_NAMES[-1]

    print(f"")
    print(f"Ayanamsa: {ayanamsa:.4f}°")
    print(f"Moon's Sidereal Longitude: {moon_sidereal_longitude:.4f}°")
    print(f"Nakshatra: {nakshatra}")

kerala = Topos(latitude=8.5, longitude=77.0)

get_nakshatra(
    datetime= datetime(2026,5,7,6,0,0),
    location=kerala,
)


print(NAKSHATRA_BOUNDARIES)
