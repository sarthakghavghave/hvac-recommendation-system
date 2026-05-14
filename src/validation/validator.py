def validate_building_input(features):

    warnings = []

    area = features.get("area_sqft")
    occupancy = features.get("occupancy")

    if area and occupancy:
        density = area / occupancy

        if density < 25:
            warnings.append(
                "Occupancy density appears unusually high "
                "for the provided building area."
            )

        elif density > 500:
            warnings.append(
                "Occupancy density appears unusually low "
                "for a commercial office building."
            )

    return warnings