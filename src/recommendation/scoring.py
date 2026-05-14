HVAC_SCORES = {

    "VRF": {
        "Energy Efficiency": 88,
        "Operational Scalability": 92,
        "Maintenance Simplicity": 65,
        "Installation Complexity": 78,
        "Zoning Flexibility": 95
    },

    "Multi-Split": {
        "Energy Efficiency": 72,
        "Operational Scalability": 68,
        "Maintenance Simplicity": 76,
        "Installation Complexity": 58,
        "Zoning Flexibility": 74
    },

    "Central Chiller": {
        "Energy Efficiency": 94,
        "Operational Scalability": 96,
        "Maintenance Simplicity": 52,
        "Installation Complexity": 95,
        "Zoning Flexibility": 70
    },

    "Split AC": {
        "Energy Efficiency": 58,
        "Operational Scalability": 40,
        "Maintenance Simplicity": 84,
        "Installation Complexity": 32,
        "Zoning Flexibility": 45
    },

    "Packaged Unit": {
        "Energy Efficiency": 66,
        "Operational Scalability": 74,
        "Maintenance Simplicity": 62,
        "Installation Complexity": 60,
        "Zoning Flexibility": 58
    }
}


def get_hvac_scores(system):
    return HVAC_SCORES.get(system, {})