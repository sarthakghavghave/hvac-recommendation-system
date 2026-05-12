VALID_BUILDINGS = [
    "Residential",
    "Office",
    "Retail",
    "Hospital",
    "Industrial"
]

VALID_CLIMATE = [
    "Hot",
    "Warm",
    "Cold",
    "Humid"
]

VALID_BUDGET = [
    "Low",
    "Medium",
    "High"
]

VALID_INSULATION = [
    "Poor",
    "Average",
    "Good",
    "Excellent"
]

VALID_GLASS = [
    "Low",
    "Medium",
    "High"
]


def validate_extracted_json(data):

    if data.get("building_type") not in VALID_BUILDINGS:
        data["building_type"] = None

    if data.get("climate_zone") not in VALID_CLIMATE:
        data["climate_zone"] = None

    if data.get("budget_level") not in VALID_BUDGET:
        data["budget_level"] = None

    if data.get("insulation") not in VALID_INSULATION:
        data["insulation"] = None

    if data.get("glass_ratio") not in VALID_GLASS:
        data["glass_ratio"] = None

    return data