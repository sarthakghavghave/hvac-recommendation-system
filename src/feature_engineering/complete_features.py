from copy import deepcopy

def complete_hvac_features(data):

    data = deepcopy(data)

    building_type = data["building_type"]["value"]
    climate_zone = data["climate_zone"]["value"]
    budget_level = data["budget_level"]["value"]

    ceiling_defaults = {
        "Residential": 9,
        "Office": 11,
        "Retail": 14,
        "Hospital": 12,
        "Industrial": 20
    }

    if data["ceiling_height"]["value"] is None:

        if building_type in ceiling_defaults:

            data["ceiling_height"] = {
                "value": ceiling_defaults[building_type],
                "source": "inferred"
            }

    operating_defaults = {
        "Residential": 10,
        "Office": 10,
        "Retail": 14,
        "Hospital": 24,
        "Industrial": 18
    }

    if data["operating_hours"]["value"] is None:

        if building_type in operating_defaults:

            data["operating_hours"] = {
                "value": operating_defaults[building_type],
                "source": "inferred"
            }

    age_defaults = {
        "Residential": 20,
        "Office": 25,
        "Retail": 15,
        "Hospital": 30,
        "Industrial": 28
    }

    if data["building_age"]["value"] is None:

        if building_type in age_defaults:

            data["building_age"] = {
                "value": age_defaults[building_type],
                "source": "inferred"
            }

    climate_defaults = {

        "Hot": {
            "outdoor_temp": 38,
            "humidity": 40
        },

        "Warm": {
            "outdoor_temp": 30,
            "humidity": 50
        },

        "Cold": {
            "outdoor_temp": 15,
            "humidity": 35
        },

        "Humid": {
            "outdoor_temp": 33,
            "humidity": 85
        }
    }

    if climate_zone in climate_defaults:

        if data["outdoor_temp"]["value"] is None:

            data["outdoor_temp"] = {
                "value": climate_defaults[climate_zone]["outdoor_temp"],
                "source": "derived"
            }

        if data["humidity"]["value"] is None:

            data["humidity"] = {
                "value": climate_defaults[climate_zone]["humidity"],
                "source": "derived"
            }

    if data["insulation"]["value"] is None:

        if budget_level == "Low":

            insulation = "Poor"

        elif budget_level == "Medium":

            insulation = "Average"

        elif budget_level == "High":

            insulation = "Good"

        else:

            insulation = "Average"

        data["insulation"] = {
            "value": insulation,
            "source": "inferred"
        }

    if data["glass_ratio"]["value"] is None:

        if building_type in ["Office", "Retail"]:

            glass = "High"

        elif building_type == "Industrial":

            glass = "Low"

        else:

            glass = "Medium"

        data["glass_ratio"] = {
            "value": glass,
            "source": "inferred"
        }

    return data