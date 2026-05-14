def generate_business_metrics(recommendation,features):

    area = features["area_sqft"]
    occupancy = features["occupancy"]
    operating_hours = features["operating_hours"]

    budget = str(features["budget_level"]).split(".")[-1]

    metrics = {}

    # VRF
    if recommendation == "VRF":

        metrics = {

            "Energy Efficiency":
                "High",

            "Estimated Energy Savings":
                "18% - 28%",

            "Installation Complexity":
                "High",

            "Maintenance Requirement":
                "Medium",

            "Operational Scalability":
                "Excellent",

            "Best Fit":
                "Multi-floor commercial buildings",

            "Long-Term Cost Efficiency":
                "Strong",

            "Expected Cooling Control":
                "Zone-level intelligent cooling"
        }

    # MULTI-SPLIT
    elif recommendation == "Multi-Split":

        metrics = {

            "Energy Efficiency":
                "Moderate to High",

            "Estimated Energy Savings":
                "10% - 18%",

            "Installation Complexity":
                "Medium",

            "Maintenance Requirement":
                "Medium",

            "Operational Scalability":
                "Moderate",

            "Best Fit":
                "Medium-sized commercial spaces",

            "Long-Term Cost Efficiency":
                "Balanced",

            "Expected Cooling Control":
                "Independent room-level cooling"
        }

    # CENTRAL CHILLER
    elif recommendation == "Central Chiller":

        metrics = {

            "Energy Efficiency":
                "Very High",

            "Estimated Energy Savings":
                "25% - 40%",

            "Installation Complexity":
                "Very High",

            "Maintenance Requirement":
                "High",

            "Operational Scalability":
                "Excellent",

            "Best Fit":
                "Large campuses and hospitals",

            "Long-Term Cost Efficiency":
                "Excellent at scale",

            "Expected Cooling Control":
                "Centralized large-scale cooling"
        }

    # SPLIT AC
    elif recommendation == "Split AC":

        metrics = {

            "Energy Efficiency":
                "Moderate",

            "Estimated Energy Savings":
                "5% - 10%",

            "Installation Complexity":
                "Low",

            "Maintenance Requirement":
                "Low",

            "Operational Scalability":
                "Limited",

            "Best Fit":
                "Small buildings and localized spaces",

            "Long-Term Cost Efficiency":
                "Moderate",

            "Expected Cooling Control":
                "Basic room-level cooling"
        }

    # PACKAGED UNIT
    elif recommendation == "Packaged Unit":

        metrics = {

            "Energy Efficiency":
                "Moderate",

            "Estimated Energy Savings":
                "8% - 15%",

            "Installation Complexity":
                "Medium",

            "Maintenance Requirement":
                "Medium",

            "Operational Scalability":
                "Good",

            "Best Fit":
                "Commercial retail and industrial spaces",

            "Long-Term Cost Efficiency":
                "Balanced",

            "Expected Cooling Control":
                "Commercial centralized cooling"
        }

    # CONTEXTUAL ADJUSTMENTS

    # Heavy occupancy bonus
    if occupancy is not None and occupancy >= 1000:
        metrics["Cooling Demand"] = ("High occupancy cooling load detected")

    # Long operational hours
    if operating_hours is not None and operating_hours >= 14:
        metrics["Operational Note"] = (
            "Extended operating hours increase "
            "importance of energy-efficient operation"
        )

    # Budget note
    if budget is not None and budget == "Low":
        metrics["Budget Impact"] = ("Lower upfront investment prioritized")

    elif budget is not None and budget == "High":
        metrics["Budget Impact"] = ("Higher efficiency investment feasible")

    return metrics