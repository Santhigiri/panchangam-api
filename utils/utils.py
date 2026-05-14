from datetime import datetime
import pytz
from core.constants import NAKSHATRA_BOUNDARIES, NAKSHATRA_NAMES, NAKSHATRA_NAMES_ML


def calc_nakshatra_from_lon(longitude: float)-> str:
    for i, boundary in enumerate(NAKSHATRA_BOUNDARIES):
        if longitude < boundary:
            nakshatra = NAKSHATRA_NAMES_ML[i]
            break
    else:
        nakshatra = NAKSHATRA_NAMES_ML[-1]

    return nakshatra

def get_localdtz(localdt: datetime, timezone: str):
    return pytz.timezone(timezone).localize(localdt)
