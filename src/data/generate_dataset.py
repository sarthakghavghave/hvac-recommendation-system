import numpy as np
import pandas as pd
import random
from pathlib import Path

PROJECT_ROOT = Path().resolve()
print("Project Root:", PROJECT_ROOT)
np.random.seed(42)
random.seed(42)

NUM_ROWS = 20000

dataset = []

building_types = {
    "Residential": 0.40,
    "Office": 0.25,
    "Retail": 0.15,
    "Hospital": 0.10,
    "Industrial": 0.10
}

climate_zones = {
    "Hot": 0.35,
    "Warm": 0.30,
    "Cold": 0.15,
    "Humid": 0.20
}

budget_levels = {
    "Low": 0.35,
    "Medium": 0.45,
    "High": 0.20
}

# Factors
climate_factor = {
    "Cold": 0.8,
    "Warm": 1.0,
    "Hot": 1.35,
    "Humid": 1.2
}

insulation_factor = {
    "Poor": 1.4,
    "Average": 1.0,
    "Good": 0.8,
    "Excellent": 0.65
}

ventilation_factor = {
    "Poor": 1.2,
    "Standard": 1.0,
    "Smart": 0.85
}

glass_factor = {
    "Low": 0.9,
    "Medium": 1.0,
    "High": 1.2
}

def weighted_choice(data):
    return np.random.choice(
        list(data.keys()),
        p=list(data.values())
    )

def generate_area(building_type):

    params = {
        "Residential": (1800, 700),
        "Office": (25000, 12000),
        "Retail": (40000, 18000),
        "Hospital": (120000, 40000),
        "Industrial": (80000, 30000)
    }

    mean, std = params[building_type]
    return max(500, np.random.normal(mean, std))

def generate_floors(area_sqft):
    floors = int(area_sqft / 15000 + np.random.normal(0, 1))
    return max(1, floors)

def generate_occupancy(building_type, area_sqft):

    density_map = {
        "Residential": 0.02,
        "Office": 0.08,
        "Retail": 0.12,
        "Hospital": 0.10,
        "Industrial": 0.05
    }

    density = density_map[building_type]
    occupancy = area_sqft * density
    occupancy *= np.random.normal(1, 0.15)
    return max(1, int(occupancy))

def generate_operating_hours(building_type):

    hours_map = {
        "Residential": (6, 14),
        "Office": (8, 12),
        "Retail": (10, 16),
        "Hospital": (20, 24),
        "Industrial": (12, 24)
    }
    low, high = hours_map[building_type]
    return np.random.randint(low, high)

def generate_climate_features(climate_zone):

    climate_data = {
        "Hot": (38, 40),
        "Warm": (30, 50),
        "Cold": (15, 35),
        "Humid": (33, 85)
    }

    temp_mean, humidity_mean = climate_data[climate_zone]
    outdoor_temp = np.random.normal(temp_mean, 3)
    humidity = np.random.normal(humidity_mean, 8)
    return outdoor_temp, humidity

def generate_insulation(budget):

    if budget == "Low":
        return np.random.choice(
            ["Poor", "Average"],
            p=[0.6, 0.4]
        )
    elif budget == "Medium":
        return np.random.choice(
            ["Average", "Good"],
            p=[0.6, 0.4]
        )
    else:
        return np.random.choice(
            ["Good", "Excellent"],
            p=[0.4, 0.6]
        )

def generate_ventilation(budget):
    if budget == "High":
        return np.random.choice(
            ["Standard", "Smart"],
            p=[0.3, 0.7]
        )
    return np.random.choice(
        ["Poor", "Standard"],
        p=[0.4, 0.6]
    )

def generate_glass_ratio(building_type):

    if building_type in ["Office", "Retail"]:
        return np.random.choice(
            ["Medium", "High"],
            p=[0.5, 0.5]
        )

    return np.random.choice(
        ["Low", "Medium"],
        p=[0.6, 0.4]
    )

# Hidden Latent Engineering Variables

# Heat gain
def calculate_heat_gain(
    area_sqft,
    climate_zone,
    occupancy,
    insulation,
    glass_ratio,
    ventilation
):

    base_heat = area_sqft * climate_factor[climate_zone]

    occupancy_heat = 1 + (occupancy / 1000)

    insulation_heat = insulation_factor[insulation]

    glass_heat = glass_factor[glass_ratio]

    ventilation_heat = ventilation_factor[ventilation]

    heat_gain = (
        base_heat
        * occupancy_heat
        * insulation_heat
        * glass_heat
        * ventilation_heat
    )

    return heat_gain

# Cooling load
def calculate_cooling_load(heat_gain):
    cooling_load = heat_gain * np.random.normal(1, 0.08)
    return cooling_load

# Tonnage estimation
def estimate_tonnage(cooling_load):
    tonnage = cooling_load / 12000
    return round(tonnage, 2)

# Energy consumption estimation
def estimate_energy(tonnage, operating_hours, climate_zone):
    energy = (
        tonnage * operating_hours * climate_factor[climate_zone] * 30
    )
    energy *= np.random.normal(1, 0.1)
    return round(energy, 2)

# HVAC
def recommend_hvac( tonnage, floors, area_sqft, building_type):

    if tonnage < 5:
        hvac = "Split AC"

    elif tonnage < 20:
        hvac = "Multi-Split"

    elif floors > 3 and tonnage < 100:
        hvac = "VRF"

    elif area_sqft > 100000:
        hvac = "Central Chiller"

    else:
        hvac = "Packaged Unit"

    # overlap / randomness
    if hvac == "VRF" and np.random.rand() < 0.10:
        hvac = "Packaged Unit"

    if hvac == "Multi-Split" and np.random.rand() < 0.08:
        hvac = "VRF"

    return hvac

# Installation cost estimation
def estimate_cost(hvac, tonnage):

    cost_per_ton = {
        "Split AC": 50000,
        "Multi-Split": 80000,
        "VRF": 120000,
        "Packaged Unit": 100000,
        "Central Chiller": 180000
    }

    cost = tonnage * cost_per_ton[hvac]
    cost *= np.random.normal(1, 0.1)

    return round(cost, 2)

# Efficiency score calculation
def efficiency_score(insulation, ventilation, energy):
    score = 100
    score -= energy / 100
    if insulation == "Poor":
        score -= 15
    if ventilation == "Poor":
        score -= 10

    return max(1, min(100, round(score)))

# Anomaly injection
def inject_anomalies(occupancy, energy, cooling_load):

    # 3% anomaly chance
    if np.random.rand() < 0.03:
        occupancy *= np.random.uniform(1.5, 3)
        energy *= np.random.uniform(1.5, 2.5)
        cooling_load *= np.random.uniform(1.5, 2)
    return occupancy, energy, cooling_load

# Generation
for _ in range(NUM_ROWS):
    # Root Variables
    building_type = weighted_choice(building_types)
    climate_zone = weighted_choice(climate_zones)
    budget_level = weighted_choice(budget_levels)

    # Structural Building Features
    area_sqft = round(generate_area(building_type), 2)
    floors = generate_floors(area_sqft)
    occupancy = generate_occupancy(building_type, area_sqft)

    operating_hours = generate_operating_hours(building_type)
    outdoor_temp, humidity = generate_climate_features(climate_zone)
    insulation = generate_insulation(budget_level)
    
    ventilation = generate_ventilation(budget_level)
    glass_ratio = generate_glass_ratio(building_type)

    # Hidden Engineering Variables
    heat_gain = calculate_heat_gain(
        area_sqft,
        climate_zone,
        occupancy,
        insulation,
        glass_ratio,
        ventilation
    )

    cooling_load = calculate_cooling_load(heat_gain)
    tonnage = estimate_tonnage(cooling_load)

    # Business Variables
    energy_consumption = estimate_energy(
        tonnage,
        operating_hours,
        climate_zone
    )

    # Anomalies
    occupancy, energy_consumption, cooling_load = inject_anomalies(
        occupancy,
        energy_consumption,
        cooling_load
    )

    # TARGET LABEL
    recommended_hvac = recommend_hvac(
        tonnage,
        floors,
        area_sqft,
        building_type
    )

    installation_cost = estimate_cost(
        recommended_hvac,
        tonnage
    )

    efficiency = efficiency_score(
        insulation,
        ventilation,
        energy_consumption
    )

    # FINAL ROW
    row = {
        # Root variables
        "building_type": building_type,
        "climate_zone": climate_zone,
        "budget_level": budget_level,

        # Building features
        "area_sqft": area_sqft,
        "floors": floors,
        "occupancy": occupancy,
        "operating_hours": operating_hours,

        # Climate
        "outdoor_temp": round(outdoor_temp, 2),
        "humidity": round(humidity, 2),

        # Envelope
        "insulation": insulation,
        "ventilation": ventilation,
        "glass_ratio": glass_ratio,

        # Hidden engineering variables
        "heat_gain": round(heat_gain, 2),
        "cooling_load": round(cooling_load, 2),

        # HVAC metrics
        "tonnage": tonnage,
        "energy_consumption": energy_consumption,
        "installation_cost": installation_cost,
        "efficiency_score": efficiency,

        # Target
        "recommended_hvac": recommended_hvac
    }

    dataset.append(row)

df = pd.DataFrame(dataset)

for col in df.columns:
    mask = np.random.rand(len(df)) < 0.02
    df.loc[mask, col] = np.nan

# Saving
df.to_csv(PROJECT_ROOT / "data/raw/hvac_synthetic_dataset.csv", index=False)

print(df.head())
print("\nDataset Shape:", df.shape)
print("\nHVAC Distribution:")
print(df["recommended_hvac"].value_counts())