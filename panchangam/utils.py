from panchangam.constants import NAKSHATRA_BOUNDARIES, NAKSHATRA_NAMES, NAKSHATRA_NAMES_ML


def calc_nakshatra_from_lon(longitude: float)-> str:
    for i, boundary in enumerate(NAKSHATRA_BOUNDARIES):
        if longitude < boundary:
            nakshatra = NAKSHATRA_NAMES_ML[i]
            break
    else:
        nakshatra = NAKSHATRA_NAMES_ML[-1]

    return nakshatra
