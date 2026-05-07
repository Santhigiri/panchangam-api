from panchangam.constants import NAKSHATRA_BOUNDARIES, NAKSHATRA_NAMES


def calc_nakshatra_from_lon(longitude: float)-> str:
    for i, boundary in enumerate(NAKSHATRA_BOUNDARIES):
        if longitude < boundary:
            nakshatra = NAKSHATRA_NAMES[i]
            break
    else:
        nakshatra = NAKSHATRA_NAMES[-1]

    return nakshatra
