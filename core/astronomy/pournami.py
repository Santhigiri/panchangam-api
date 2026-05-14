from datetime import datetime
from .thithi import get_thithi

def is_poornima(localdt: datetime, timezone: str)-> bool:
    night_time = datetime(
        year=localdt.year,
        month=localdt.month,
        day=localdt.day,
        hour=23,
        minute=59,
        second=59
    )
    thithi = get_thithi(night_time, timezone)
    return thithi == "Pournami"
