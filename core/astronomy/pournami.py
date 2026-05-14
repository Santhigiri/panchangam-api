from datetime import datetime, timedelta
from .thithi import get_thithi


def get_day_end_thithi(localdt: datetime, timezone: str)-> str:
    night_time = datetime(
        year=localdt.year,
        month=localdt.month,
        day=localdt.day,
        hour=23,
        minute=59,
        second=59
    )
    thithi = get_thithi(night_time, timezone)
    return thithi


def is_poornima(localdt: datetime, timezone: str)-> bool:
    previous_day = localdt - timedelta(days=-1)
    previous_day_thithi = get_day_end_thithi(previous_day, timezone)
    current_day_thithi = get_day_end_thithi(localdt, timezone)
    return current_day_thithi == "Pournami" and previous_day_thithi != "Pournami"
