import numpy as np
import pandas as pd
import random
from pathlib import Path

np.random.seed(42)
random.seed(42)

PROJECT_ROOT = Path().resolve()

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
        "Retail": (45000, 22000),
        "Hospital": (120000, 50000),
        "Industrial": (80000, 35000)
    }

    mean, std = params[building_type]

    area = np.random.normal(mean, std)

    return max(500, area)

def generate_floors(area_sqft):

    floors = (
        area_sqft / 18000
        + np.random.normal(0, 1.5)
    )

    return max(1, int(floors))

def generate_occupancy(building_type, area_sqft):

    density_map = {
        "Residential": 0.02,
        "Office": 0.08,
        "Retail": 0.12,
        "Hospital": 0.10,
        "Industrial": 0.05
    }

    occupancy_behavior = np.random.normal(1, 0.25)

    occupancy = (
        area_sqft
        * density_map[building_type]
        * occupancy_behavior
    )

    return max(1, int(occupancy))

def generate_operating_hours(building_type):

    ranges = {
        "Residential": (6, 14),
        "Office": (8, 12),
        "Retail": (10, 16),
        "Hospital": (20, 24),
        "Industrial": (12, 24)
    }

    low, high = ranges[building_type]

    return np.random.randint(low, high)

def generate_building_age(building_type):

    params = {
        "Residential": (20, 12),
        "Office": (25, 15),
        "Retail": (15, 10),
        "Hospital": (30, 18),
        "Industrial": (28, 15)
    }

    mean, std = params[building_type]

    age = np.random.normal(mean, std)

    return max(0, int(age))

def generate_climate(climate_zone):

    climate_data = {
        "Hot": (38, 40),
        "Warm": (30, 50),
        "Cold": (15, 35),
        "Humid": (33, 85)
    }

    temp_mean, humidity_mean = climate_data[climate_zone]

    outdoor_temp = np.random.normal(temp_mean, 4)

    humidity = np.random.normal(humidity_mean, 10)

    return outdoor_temp, humidity

def generate_insulation(budget_level, building_age):

    if budget_level == "Low":

        probs = [0.6, 0.4, 0.0, 0.0]

    elif budget_level == "Medium":

        probs = [0.15, 0.5, 0.35, 0.0]

    else:

        probs = [0.0, 0.2, 0.5, 0.3]

    insulation = np.random.choice(
        ["Poor", "Average", "Good", "Excellent"],
        p=probs
    )

    if building_age > 40 and np.random.rand() < 0.4:

        insulation = np.random.choice(
            ["Poor", "Average"],
            p=[0.7, 0.3]
        )

    return insulation

def generate_glass_ratio(building_type):

    if building_type in ["Office", "Retail"]:

        return np.random.choice(
            ["Medium", "High"],
            p=[0.45, 0.55]
        )

    return np.random.choice(
        ["Low", "Medium"],
        p=[0.7, 0.3]
    )

def calculate_heat_gain(
    area_sqft,
    climate_zone,
    occupancy,
    insulation,
    glass_ratio,
    building_age
):

    occupancy_factor = 1 + (occupancy / 1000)

    age_factor = np.random.normal(
        1 + (building_age / 120),
        0.10
    )

    random_building_behavior = np.random.normal(1, 0.18)

    heat_gain = (
        area_sqft
        * climate_factor[climate_zone]
        * occupancy_factor
        * insulation_factor[insulation]
        * glass_factor[glass_ratio]
        * age_factor
        * random_building_behavior
    )

    return heat_gain

def calculate_cooling_load(
    heat_gain,
    building_age
):

    operational_variation = np.random.normal(1, 0.18)

    occupancy_behavior = np.random.normal(1, 0.20)

    ventilation_loss = np.random.normal(1, 0.15)

    equipment_degradation = np.random.normal(
        1 + (building_age / 180),
        0.12
    )

    control_efficiency = np.random.normal(1, 0.18)

    cooling_load = (
        heat_gain
        * operational_variation
        * occupancy_behavior
        * ventilation_loss
        * equipment_degradation
        * control_efficiency
    )

    return cooling_load

def estimate_tonnage(cooling_load):

    oversizing_factor = np.random.normal(1.15, 0.25)

    installer_preference = np.random.normal(1, 0.15)

    tonnage = (
        cooling_load / 12000
    ) * oversizing_factor * installer_preference

    return round(tonnage, 2)

def estimate_energy(
    tonnage,
    operating_hours,
    climate_zone,
    building_age
):

    occupancy_behavior = np.random.normal(1, 0.20)

    control_efficiency = np.random.normal(1, 0.18)

    partial_load_factor = np.random.normal(1, 0.15)

    age_penalty = np.random.normal(
        1 + (building_age / 160),
        0.12
    )

    energy = (
        tonnage
        * operating_hours
        * climate_factor[climate_zone]
        * occupancy_behavior
        * control_efficiency
        * partial_load_factor
        * age_penalty
        * 30
    )

    energy *= np.random.normal(1, 0.15)

    return round(energy, 2)

def softmax(x):

    e_x = np.exp(x - np.max(x))

    return e_x / e_x.sum()

def recommend_hvac(
    tonnage,
    floors,
    area_sqft,
    building_type,
    budget_level,
    building_age
):

    scores = {
        "Split AC": 0,
        "Multi-Split": 0,
        "VRF": 0,
        "Packaged Unit": 0,
        "Central Chiller": 0
    }

    # Tonnage influence

    if tonnage < 5:
        scores["Split AC"] += 5

    if 5 <= tonnage < 20:
        scores["Multi-Split"] += 4

    if 15 <= tonnage < 80:
        scores["VRF"] += 4

    if 20 <= tonnage <= 60:
        scores["Packaged Unit"] += 4

    if tonnage > 70:
        scores["Central Chiller"] += 5

    # Floors

    if floors > 3:
        scores["VRF"] += 3

    if floors <= 3 and area_sqft > 30000:
        scores["Packaged Unit"] += 3

    if floors > 8:
        scores["Central Chiller"] += 2

    # Building type

    if building_type == "Hospital":
        scores["Central Chiller"] += 5

    if building_type == "Industrial":
        scores["Packaged Unit"] += 4

    if building_type == "Retail":
        scores["Packaged Unit"] += 3

    if building_type == "Residential":
        scores["Split AC"] += 4

    # Budget

    if budget_level == "Low":
        scores["Split AC"] += 3

    if budget_level == "Medium":
        scores["Packaged Unit"] += 2

    if budget_level == "High":
        scores["VRF"] += 2
        scores["Central Chiller"] += 2

    # Building age

    if building_age > 40:

        scores["Split AC"] += 2

        scores["Packaged Unit"] += 2

        scores["Central Chiller"] -= 2

    labels = list(scores.keys())

    values = np.array(list(scores.values()))

    temperature = 2.5

    probs = softmax(values / temperature)

    hvac = np.random.choice(labels, p=probs)

    # Recommendation randomness
    if np.random.rand() < 0.08:

        hvac = np.random.choice([
            "VRF",
            "Packaged Unit",
            "Multi-Split"
        ])

    return hvac

def estimate_cost(hvac, tonnage):

    cost_map = {
        "Split AC": 50000,
        "Multi-Split": 80000,
        "VRF": 120000,
        "Packaged Unit": 100000,
        "Central Chiller": 180000
    }

    base_cost = tonnage * cost_map[hvac]

    retrofit_complexity = np.random.normal(1, 0.30)

    brand_premium = np.random.normal(1, 0.20)

    material_variation = np.random.normal(1, 0.15)

    regional_variation = np.random.normal(1, 0.18)

    cost = (
        base_cost
        * retrofit_complexity
        * brand_premium
        * material_variation
        * regional_variation
    )

    return round(cost, 2)

def efficiency_score(
    insulation,
    energy_consumption,
    building_age
):

    operational_quality = np.random.normal(1, 0.15)

    score = (
        100
        - (energy_consumption / 150)
    ) * operational_quality

    if insulation == "Poor":
        score -= 15

    if building_age > 40:
        score -= 10

    return max(1, min(100, round(score)))

def inject_anomalies(
    occupancy,
    energy_consumption,
    cooling_load,
    tonnage
):

    if np.random.rand() < 0.04:

        occupancy *= np.random.uniform(1.5, 3)

        energy_consumption *= np.random.uniform(1.5, 2.8)

        cooling_load *= np.random.uniform(1.4, 2.2)

        tonnage *= np.random.uniform(1.3, 2)

    return (
        occupancy,
        energy_consumption,
        cooling_load,
        tonnage
    )

for _ in range(NUM_ROWS):

    building_type = weighted_choice(building_types)

    climate_zone = weighted_choice(climate_zones)

    budget_level = weighted_choice(budget_levels)

    area_sqft = round(generate_area(building_type), 2)

    floors = generate_floors(area_sqft)

    occupancy = generate_occupancy(
        building_type,
        area_sqft
    )

    operating_hours = generate_operating_hours(
        building_type
    )

    building_age = generate_building_age(
        building_type
    )

    outdoor_temp, humidity = generate_climate(
        climate_zone
    )

    insulation = generate_insulation(
        budget_level,
        building_age
    )

    glass_ratio = generate_glass_ratio(
        building_type
    )

    heat_gain = calculate_heat_gain(
        area_sqft,
        climate_zone,
        occupancy,
        insulation,
        glass_ratio,
        building_age
    )

    cooling_load = calculate_cooling_load(
        heat_gain,
        building_age
    )

    tonnage = estimate_tonnage(
        cooling_load
    )

    energy_consumption = estimate_energy(
        tonnage,
        operating_hours,
        climate_zone,
        building_age
    )

    occupancy, energy_consumption, cooling_load, tonnage = inject_anomalies(
        occupancy,
        energy_consumption,
        cooling_load,
        tonnage
    )

    recommended_hvac = recommend_hvac(
        tonnage,
        floors,
        area_sqft,
        building_type,
        budget_level,
        building_age
    )

    installation_cost = estimate_cost(
        recommended_hvac,
        tonnage
    )

    efficiency = efficiency_score(
        insulation,
        energy_consumption,
        building_age
    )

    row = {

        "building_type": building_type,
        "climate_zone": climate_zone,
        "budget_level": budget_level,

        "area_sqft": round(area_sqft, 2),
        "floors": floors,
        "occupancy": occupancy,
        "operating_hours": operating_hours,
        "building_age": building_age,

        "outdoor_temp": round(outdoor_temp, 2),
        "humidity": round(humidity, 2),

        "insulation": insulation,
        "glass_ratio": glass_ratio,

        "heat_gain": round(heat_gain, 2),
        "cooling_load": round(cooling_load, 2),

        "tonnage": round(tonnage, 2),
        "energy_consumption": round(energy_consumption, 2),

        "installation_cost": round(installation_cost, 2),
        "efficiency_score": efficiency,

        "recommended_hvac": recommended_hvac
    }

    dataset.append(row)

df = pd.DataFrame(dataset)

# Missing values
for col in df.columns:

    mask = np.random.rand(len(df)) < 0.02

    df.loc[mask, col] = np.nan

# Save
output_path = PROJECT_ROOT / "data/raw/hvac_synthetic_dataset_v3.csv"

df.to_csv(output_path, index=False)

print("\nDataset Shape:", df.shape)

print("\nHVAC Distribution:")
print(df["recommended_hvac"].value_counts())

print(f"\nSaved to: {output_path}")