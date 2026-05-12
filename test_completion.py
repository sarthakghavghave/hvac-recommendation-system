from pprint import pprint

from src.feature_engineering.complete_features import complete_hvac_features

sample = {

    "building_type": "Office",
    "climate_zone": "Hot",
    "budget_level": None,

    "area_sqft": None,
    "floors": 4,
    "ceiling_height": None,

    "occupancy": 300,
    "operating_hours": None,
    "building_age": None,

    "outdoor_temp": 38,
    "humidity": 40,

    "insulation": None,
    "glass_ratio": None
}

completed = complete_hvac_features(sample)

pprint(completed)