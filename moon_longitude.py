from skyfield.api import load, Topos
from skyfield.framelib import ecliptic_frame
from datetime import datetime, timedelta
import pytz

# Load ephemeris
planets = load('de421.bsp')
earth = planets['earth']
moon = planets['moon']
ts = load.timescale()

# Kerala location (Thiruvananthapuram)
kerala = earth + Topos(latitude_degrees=8.5, longitude_degrees=77.0)

# Date: May 7, 2026
date = datetime(2026, 5, 7)
tz = pytz.timezone('Asia/Kolkata')

# Approximate sunrise in Kerala (6:00 AM IST)
sunrise = tz.localize(datetime(2026, 5, 7, 6, 0, 0))
t = ts.utc(sunrise.year, sunrise.month, sunrise.day, sunrise.hour, sunrise.minute, sunrise.second)

# Calculate Moon's position at sunrise
astrometric = kerala.at(t).observe(moon)
apparent = astrometric.apparent()
lat, lon, distance = apparent.frame_latlon(ecliptic_frame)
moon_longitude = float(lon.degrees) % 360

print(f"Moon's Longitude at Sunrise (Kerala): {moon_longitude:.4f}°")

# Nakshatra boundaries (standard)
NAKSHATRA_BOUNDARIES = [
    13.333, 26.666, 40.0, 53.333, 66.666, 80.0, 93.333, 106.666, 120.0,
    133.333, 146.666, 160.0, 173.333, 186.666, 200.0, 213.333, 226.666, 240.0,
    253.333, 266.666, 280.0, 293.333, 306.666, 320.0, 333.333, 346.666, 360.0
]
NAKSHATRA_NAMES = [
    "Aswathy", 
    "Bharani", 
    "Karthika", 
    "Rohini", 
    "Makayiram",
    "Thiruvathira", 
    "Punartham", 
    "Pooyam",
    "Aayilyam", 
    "Makam", 
    "Pooram", 
    "Uthram",
    "Atham",
    "Chithira",
    "Chothi",
    "Vishagam",
    "Anizham",
    "Thrikketta",
    "Moolam",
    "Pooradam",
    "Uthradam",
    "Thiruvonam",
    "Avittam",
    "Chathayam",
    "Poororuttathi",
    "Uthrattathi",
    "Revathi"
]

# Determine Nakshatra
for i, boundary in enumerate(NAKSHATRA_BOUNDARIES):
    if moon_longitude < boundary:
        nakshatra = NAKSHATRA_NAMES[i]
        break
else:
    nakshatra = NAKSHATRA_NAMES[-1]

print(f"Nakshatra at Sunrise (Kerala): {nakshatra}")
