def derive_missing_features(data):

    # climate defaults
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

    zone = data.get("climate_zone")

    if zone in climate_defaults:

        if data.get("outdoor_temp") is None:
            data["outdoor_temp"] = climate_defaults[zone]["outdoor_temp"]

        if data.get("humidity") is None:
            data["humidity"] = climate_defaults[zone]["humidity"]

    # default insulation
    if data.get("insulation") is None:

        budget = data.get("budget_level")

        if budget == "Low":
            data["insulation"] = "Poor"

        elif budget == "Medium":
            data["insulation"] = "Average"

        else:
            data["insulation"] = "Good"

    # default glass ratio
    if data.get("glass_ratio") is None:

        if data.get("building_type") in ["Office", "Retail"]:
            data["glass_ratio"] = "High"

        else:
            data["glass_ratio"] = "Medium"

    return data