import numpy as np
import pandas as pd
import random
from pathlib import Path

PROJECT_ROOT = Path().resolve()
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
        "Retail": (45000, 20000),
        "Hospital": (120000, 45000),
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

    occupancy = (
        area_sqft
        * density_map[building_type]
        * np.random.normal(1, 0.15)
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

    outdoor_temp = np.random.normal(temp_mean, 3)

    humidity = np.random.normal(humidity_mean, 8)

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
            p=[0.5, 0.5]
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

    age_factor = 1 + (building_age / 100)

    heat_gain = (
        area_sqft
        * climate_factor[climate_zone]
        * occupancy_factor
        * insulation_factor[insulation]
        * glass_factor[glass_ratio]
        * age_factor
    )

    return heat_gain

def calculate_cooling_load(heat_gain):

    return heat_gain * np.random.normal(1, 0.08)

def estimate_tonnage(cooling_load):

    return round(cooling_load / 12000, 2)

def estimate_energy(
    tonnage,
    operating_hours,
    climate_zone,
    building_age
):

    age_penalty = 1 + (building_age / 150)

    energy = (
        tonnage
        * operating_hours
        * climate_factor[climate_zone]
        * age_penalty
        * 30
    )

    energy *= np.random.normal(1, 0.1)

    return round(energy, 2)

def softmax(x):

    e_x = np.exp(x - np.max(x))

    return e_x / e_x.sum()

def recommend_hvac(
    tonnage,
    floors,
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

    if tonnage < 5:
        scores["Split AC"] += 5

    if 5 <= tonnage < 20:
        scores["Multi-Split"] += 5

    if 15 <= tonnage < 80:
        scores["VRF"] += 5

    if tonnage > 70:
        scores["Central Chiller"] += 6

    if floors > 3:
        scores["VRF"] += 3

    if floors > 8:
        scores["Central Chiller"] += 2

    if building_type == "Hospital":
        scores["Central Chiller"] += 5

    if building_type == "Industrial":
        scores["Packaged Unit"] += 4

    if building_type == "Residential":
        scores["Split AC"] += 4

    if budget_level == "Low":
        scores["Split AC"] += 3

    if budget_level == "High":
        scores["VRF"] += 2
        scores["Central Chiller"] += 2

    if building_age > 40:

        scores["Split AC"] += 2
        scores["Packaged Unit"] += 2

        scores["Central Chiller"] -= 2

    labels = list(scores.keys())

    values = np.array(list(scores.values()))

    probs = softmax(values)

    hvac = np.random.choice(labels, p=probs)

    confidence = round(np.max(probs) * 100, 2)

    return hvac, confidence

def estimate_cost(hvac, tonnage):

    cost_map = {
        "Split AC": 50000,
        "Multi-Split": 80000,
        "VRF": 120000,
        "Packaged Unit": 100000,
        "Central Chiller": 180000
    }

    cost = tonnage * cost_map[hvac]

    cost *= np.random.normal(1, 0.1)

    return round(cost, 2)

def efficiency_score(
    insulation,
    energy_consumption,
    building_age
):

    score = 100

    score -= energy_consumption / 120

    if insulation == "Poor":
        score -= 15

    if building_age > 40:
        score -= 10

    return max(1, min(100, round(score)))

def inject_anomalies(
    occupancy,
    energy_consumption,
    cooling_load
):

    if np.random.rand() < 0.03:

        occupancy *= np.random.uniform(1.5, 3)

        energy_consumption *= np.random.uniform(1.5, 2.5)

        cooling_load *= np.random.uniform(1.5, 2)

    return occupancy, energy_consumption, cooling_load

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
        heat_gain
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

    occupancy, energy_consumption, cooling_load = inject_anomalies(
        occupancy,
        energy_consumption,
        cooling_load
    )

    recommended_hvac, confidence = recommend_hvac(
        tonnage,
        floors,
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

        "area_sqft": area_sqft,
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

        "tonnage": tonnage,
        "energy_consumption": energy_consumption,

        "installation_cost": installation_cost,
        "efficiency_score": efficiency,

        "recommendation_confidence": confidence,

        "recommended_hvac": recommended_hvac
    }

    dataset.append(row)

df = pd.DataFrame(dataset)

for col in df.columns:

    mask = np.random.rand(len(df)) < 0.02

    df.loc[mask, col] = np.nan

df.to_csv(PROJECT_ROOT / "data/raw/hvac_synthetic_dataset_v2.csv", index=False)

print(df.head())

print("\nDataset Shape:", df.shape)

print("\nHVAC Distribution:")
print(df["recommended_hvac"].value_counts())