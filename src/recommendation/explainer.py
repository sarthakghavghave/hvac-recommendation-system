def generate_recommendation_summary(recommendation,features,top_recommendations):

    building_type = str(features["building_type"]).split(".")[-1]

    area = features["area_sqft"]
    floors = features["floors"]
    occupancy = features["occupancy"]

    budget = str(features["budget_level"]).split(".")[-1]

    operating_hours = features["operating_hours"]
    summary = []
    tradeoffs = []

    # PRIMARY RECOMMENDATION LOGIC
    if recommendation == "VRF":

        summary.append(
            "VRF systems are suitable for "
            "multi-floor commercial buildings "
            "where zoning flexibility and "
            "energy-efficient cooling are important."
        )

        if floors is not None and floors >= 3:

            summary.append(
                f"The {floors}-floor layout benefits "
                "from independent zone-level cooling control."
            )

        if occupancy is not None and occupancy >= 500:

            summary.append(
                "The high occupancy load requires "
                "scalable cooling distribution across spaces."
            )

        if operating_hours is not None and operating_hours >= 10:

            summary.append(
                "Long operating hours increase the "
                "importance of part-load efficiency "
                "and operational optimization."
            )

        if budget is not None and budget == "High":

            summary.append(
                "The higher upfront investment aligns "
                "with long-term operational efficiency benefits."
            )

        # Comparative Reasoning
        tradeoffs.append(
            "Central Chiller was not preferred because "
            "the building scale does not fully justify "
            "large centralized cooling infrastructure."
        )

        tradeoffs.append(
            "Multi-Split systems may reduce initial "
            "installation cost but offer less efficient "
            "large-scale zoning and control."
        )

    # MULTI-SPLIT
    elif recommendation == "Multi-Split":

        summary.append(
            "Multi-Split systems are effective for "
            "medium-sized buildings requiring moderate "
            "zoning flexibility with lower infrastructure complexity."
        )

        if area is not None and area < 15000:

            summary.append(
                "The building size remains within a "
                "practical range for distributed cooling deployment."
            )

        if floors is not None and floors <= 4:

            summary.append(
                "The building height is manageable "
                "without requiring centralized HVAC systems."
            )

        if budget is not None and budget == "Medium":

            summary.append(
                "The medium budget aligns well with "
                "the installation and maintenance profile "
                "of multi-split systems."
            )

        tradeoffs.append(
            "VRF systems may provide higher efficiency "
            "for large-scale zoning but would increase "
            "installation cost significantly."
        )

        tradeoffs.append(
            "Central Chiller systems were not preferred "
            "because the building scale is insufficient "
            "to justify centralized thermal infrastructure."
        )

    # CENTRAL CHILLER
    elif recommendation == "Central Chiller":

        summary.append(
            "Central Chiller systems are suitable for "
            "large buildings with continuous cooling demand "
            "and centralized thermal management requirements."
        )

        if area is not None and area >= 100000:

            summary.append(
                "The large building footprint supports "
                "economies of scale for centralized cooling."
            )

        if occupancy is not None and occupancy >= 2000:

            summary.append(
                "The high occupancy load requires "
                "high-capacity centralized cooling infrastructure."
            )

        if operating_hours is not None and operating_hours >= 18:

            summary.append(
                "Continuous operational demand favors "
                "centralized cooling efficiency."
            )

        tradeoffs.append(
            "VRF systems may provide zoning flexibility "
            "but become operationally complex at this scale."
        )

        tradeoffs.append(
            "Multi-Split systems were not preferred due "
            "to maintenance complexity across large installations."
        )

    # SPLIT AC
    elif recommendation == "Split AC":

        summary.append(
            "Split AC systems are appropriate for "
            "smaller buildings with localized cooling needs."
        )

        if area is not None and area < 3000:

            summary.append(
                "The building size does not justify "
                "centralized HVAC infrastructure."
            )

        if budget is not None and budget == "Low":

            summary.append(
                "The lower budget aligns with the "
                "cost-effective installation profile "
                "of split AC systems."
            )

        tradeoffs.append(
            "VRF systems would increase installation "
            "cost without proportional operational benefits."
        )

        tradeoffs.append(
            "Packaged or centralized systems would "
            "introduce unnecessary infrastructure complexity."
        )

    # PACKAGED UNIT
    elif recommendation == "Packaged Unit":

        summary.append(
            "Packaged HVAC systems are practical for "
            "commercial spaces requiring simpler deployment "
            "and moderate centralized cooling."
        )

        if operating_hours is not None and operating_hours >= 12:

            summary.append(
                "Extended operational hours require "
                "robust commercial HVAC capability."
            )

        if building_type is not None and building_type in ["Retail", "Industrial"]:

            summary.append(
                "Commercial occupancy patterns align "
                "well with packaged HVAC operation."
            )

        tradeoffs.append(
            "VRF systems may provide higher zoning "
            "efficiency but increase installation complexity."
        )

        tradeoffs.append(
            "Central Chiller infrastructure would "
            "not be operationally efficient at this scale."
        )

    # ALTERNATIVE RECOMMENDATIONS
    alternatives = []
    for item in top_recommendations:
        if item["system"] != recommendation:
            alternatives.append(
                f"{item['system']} "
                f"({item['confidence']}%)"
            )

    return {
        "summary": summary,
        "tradeoffs": tradeoffs,
        "alternatives": alternatives
    }