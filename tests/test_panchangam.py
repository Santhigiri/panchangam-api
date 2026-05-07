
from panchangam.panchangam import get_nakshatra


def test_get_nakshathra():
    assert get_nakshatra(20) == "Aswathi"
