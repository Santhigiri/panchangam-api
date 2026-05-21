from datetime import date, datetime
from typing import List
from pydantic import BaseModel, field_serializer
from core.astronomy.nakshatra_transition import NakshatraTransition
from core.astronomy.thithi_transition import ThithiTransition
from core.calendar.kollavarsham import KollavarshamDate
from utils.nakshatra import Nakshatra
from utils.thithi import Thithi
from typing import List, Optional
from pydantic import BaseModel
from utils.malayalam_masa import MalayalamMasa
from utils.nakshatra import Nakshatra
from utils.thithi import Thithi

class EventCondition(BaseModel):
    nakshatra: Optional[Nakshatra] = None
    thithi: Optional[Thithi] = None
    ml_day: Optional[int] = None
    ml_month: Optional[MalayalamMasa] = None
    ml_year: Optional[int] = None
    en_day: Optional[int] = None
    en_month: Optional[int] = None
    en_year: Optional[int] = None
    occurance: Optional[int] = None
    last_occurance: bool = False

class SanthigiriEvent(BaseModel):
    name: str
    description: str
    event_condition: EventCondition


class PanchangamData(BaseModel):
    date: date
    kv: KollavarshamDate
    thithi_transitions: List[ThithiTransition]
    nakshatra_transitions: List[NakshatraTransition]
    is_pournami: bool
    thithi: Thithi
    nakshatra: Nakshatra
    sunrise: datetime
    sunset: datetime
    santhigiri_significant_dates: List[SanthigiriEvent] = []

    @field_serializer("nakshatra")
    def ser_nakshatra(self, n: Nakshatra):
        return n.to_dict()
    
    @field_serializer('thithi')
    def ser_thithi(self, t: Thithi):
        return t.to_dict()



SANTHIGIRI_EVENTS: List[SanthigiriEvent] = [
    SanthigiriEvent(
        name="Navoli Jyothir Dinam",
        description="Navoli Jyothir Dinam",
        event_condition=EventCondition(
            en_day= 6,
            en_month=5
        )
    ),
    SanthigiriEvent(
        name="Janmagriha Theertha Yaathra",
        description="Janmagriha Theertha Yaathra",
        event_condition= EventCondition(
            nakshatra=Nakshatra.CHOTHI
        )
    )
]

def get_santhigiri_significant_dates(panchangam_data: PanchangamData) -> List[SanthigiriEvent]:
    occurances = []
    for event in SANTHIGIRI_EVENTS:
        condition = event.event_condition
        if condition.nakshatra is not None and condition.nakshatra != panchangam_data.nakshatra:
            continue
        if condition.thithi is not None and condition.thithi != panchangam_data.thithi:
            continue
        if condition.ml_day is not None and condition.ml_day != panchangam_data.kv.kv_day:
            continue
        if condition.ml_month is not None and condition.ml_month != panchangam_data.kv.kv_month:
            continue
        if condition.ml_year is not None and condition.ml_year != panchangam_data.kv.kv_year:
            continue
        if condition.en_day is not None and condition.en_day != panchangam_data.date.day:
            continue
        if condition.en_month is not None and condition.en_month != panchangam_data.date.month:
            continue
        if condition.en_year is not None and condition.en_year != panchangam_data.date.year:
            continue

        occurances.append(event)

    return occurances



