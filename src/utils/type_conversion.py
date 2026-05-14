NUMERIC_FIELDS = {

    "area_sqft": float,
    "floors": int,
    "ceiling_height": float,
    "occupancy": int,
    "operating_hours": int,
    "building_age": int,
    "outdoor_temp": float,
    "humidity": float
}


def convert_feature_type(field, value):

    if value is None:
        return None

    if field not in NUMERIC_FIELDS:
        return value

    try:
        return NUMERIC_FIELDS[field](value)

    except Exception:
        return None