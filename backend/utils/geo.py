from math import acos, cos, radians, sin

EARTH_RADIUS_KM = 6371


def haversine_km(lat1, lng1, lat2, lng2):
    """Distance in km between two GPS points; None when a coordinate is missing."""
    if lat1 is None or lng1 is None or lat2 is None or lng2 is None:
        return None

    angle = (
        cos(radians(lat1)) * cos(radians(lat2)) * cos(radians(lng2) - radians(lng1))
        + sin(radians(lat1)) * sin(radians(lat2))
    )
    clamped = min(1.0, max(-1.0, angle))
    return EARTH_RADIUS_KM * acos(clamped)
