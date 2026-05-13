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

def generate_ceiling_height(
    building_type,
    area_sqft
):

    ranges = {
        "Residential": (8, 11),
        "Office": (10, 14),
        "Retail": (12, 18),
        "Hospital": (10, 15),
        "Industrial": (15, 30)
    }

    low, high = ranges[building_type]

    height = np.random.uniform(low, high)

    if area_sqft > 100000:
        height *= np.random.normal(1.1, 0.08)

    return round(height, 2)

def generate_occupancy(
    building_type,
    area_sqft
):

    density_map = {
        "Residential": 0.018,
        "Office": 0.06,
        "Retail": 0.10,
        "Hospital": 0.08,
        "Industrial": 0.04
    }

    usage_mode = np.random.choice(["Sparse", "Normal", "Dense"], p=[0.2, 0.6, 0.2])

    mode_factor = {
        "Sparse": np.random.uniform(0.5, 0.8),
        "Normal": np.random.uniform(0.8, 1.2),
        "Dense": np.random.uniform(1.2, 1.8)
    }

    occupancy = area_sqft * density_map[building_type] * mode_factor[usage_mode]
    occupancy *= np.random.normal(1, 0.25)

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

def generate_insulation(
    budget_level,
    building_age
):

    if budget_level == "Low":
        probs = [0.6, 0.4, 0.0, 0.0]

    elif budget_level == "Medium":
        probs = [0.15, 0.5, 0.35, 0.0]

    else:
        probs = [0.0, 0.2, 0.5, 0.3]

    insulation = np.random.choice(["Poor", "Average", "Good", "Excellent"], p=probs)

    if building_age > 40 and np.random.rand() < 0.4:

        insulation = np.random.choice(["Poor", "Average"], p=[0.7, 0.3])

    return insulation

def generate_glass_ratio(building_type):

    if building_type in ["Office", "Retail"]:
        return np.random.choice(["Medium", "High"], p=[0.45, 0.55])

    return np.random.choice(["Low", "Medium"], p=[0.7, 0.3])

def generate_occupancy_variability(building_type):

    if building_type == "Office":
        return np.random.choice(["Low", "Medium", "High"], p=[0.2, 0.5, 0.3])

    elif building_type == "Retail":
        return np.random.choice(["Medium", "High"], p=[0.4, 0.6])

    elif building_type == "Residential":
        return np.random.choice(["Low", "Medium"], p=[0.7, 0.3])

    elif building_type == "Hospital":
        return np.random.choice(["Medium", "High"], p=[0.3, 0.7])

    return np.random.choice(["Low", "Medium", "High"], p=[0.4, 0.4, 0.2])

def generate_ventilation_requirement(building_type):

    if building_type == "Hospital":
        return np.random.choice(["Medium", "High"], p=[0.2, 0.8])

    elif building_type == "Industrial":
        return np.random.choice(["Medium", "High"], p=[0.4, 0.6])

    elif building_type == "Residential":
        return np.random.choice(["Low", "Medium"], p=[0.8, 0.2])

    return np.random.choice(["Low", "Medium", "High"], p=[0.3, 0.5, 0.2])

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def recommend_hvac(
    building_type,
    area_sqft,
    floors,
    occupancy,
    operating_hours,
    building_age,
    budget_level,
    insulation,
    glass_ratio,
    climate_zone,
    ceiling_height,
    occupancy_variability,
    ventilation_requirement
):

    scores = {
        "Split AC": 0,
        "Multi-Split": 0,
        "VRF": 0,
        "Packaged Unit": 0,
        "Central Chiller": 0
    }

    if area_sqft < 2500:
        scores["Split AC"] += 4

    if 2500 <= area_sqft < 20000:
        scores["Multi-Split"] += 4

    if 15000 <= area_sqft < 100000:
        scores["VRF"] += 4

    if 25000 <= area_sqft <= 90000:
        scores["Packaged Unit"] += 4

    if area_sqft > 100000:
        scores["Central Chiller"] += 5

    if floors > 3:
        scores["VRF"] += 3

    if floors > 8:
        scores["Central Chiller"] += 3

    if occupancy > 3000:
        scores["Central Chiller"] += 3

    elif occupancy > 1000:
        scores["VRF"] += 2

    if building_type == "Residential":
        scores["Split AC"] += 4

    if building_type == "Hospital":
        scores["Central Chiller"] += 5

    if building_type == "Industrial":
        scores["Packaged Unit"] += 4

    if building_type == "Retail":
        scores["Packaged Unit"] += 3

    if building_type in ["Residential", "Office"]:
        scores["Multi-Split"] += 2

    if operating_hours > 18:
        scores["Central Chiller"] += 2

    if ceiling_height > 15:
        scores["Packaged Unit"] += 2

    if budget_level == "Low":
        scores["Split AC"] += 3

    if budget_level == "Medium":
        scores["Packaged Unit"] += 2
        scores["Multi-Split"] += 2

    if budget_level == "High":
        scores["VRF"] += 2
        scores["Central Chiller"] += 2

    if building_age > 40:
        scores["Split AC"] += 2
        scores["Packaged Unit"] += 2
        scores["Central Chiller"] -= 2

    if insulation == "Poor":
        scores["Central Chiller"] += 1

    if glass_ratio == "High":
        scores["VRF"] += 1
        scores["Central Chiller"] += 1

    if climate_zone in ["Hot", "Humid"]:
        scores["VRF"] += 1
        scores["Central Chiller"] += 1

    if occupancy_variability == "High":
        scores["VRF"] += 3

    if occupancy_variability == "Medium":
        scores["Multi-Split"] += 2

    if ventilation_requirement == "High":
        scores["Central Chiller"] += 3

    if ventilation_requirement == "High":
        scores["Split AC"] -= 2

    if (
        ventilation_requirement == "Medium"
        and ceiling_height > 14
    ):
        scores["Packaged Unit"] += 2

    if (
        2500 <= area_sqft <= 15000
        and floors <= 3
        and occupancy <= 400
    ):
        scores["Multi-Split"] += 5
        
    labels = list(scores.keys())
    values = np.array(list(scores.values()))
    temperature = 2.5
    probs = softmax(values / temperature)
    hvac = np.random.choice(labels, p=probs)
    
    # recommendation randomness
    if np.random.rand() < 0.03:

        hvac = np.random.choice([
            "VRF",
            "Packaged Unit",
            "Multi-Split"
        ])


    return hvac

# Generation Loop
for _ in range(NUM_ROWS):

    building_type = weighted_choice(building_types)

    climate_zone = weighted_choice(climate_zones)

    budget_level = weighted_choice(budget_levels)

    area_sqft = round(
        generate_area(building_type),
        2
    )

    floors = generate_floors(area_sqft)

    ceiling_height = generate_ceiling_height(
        building_type,
        area_sqft
    )

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

    occupancy_variability = generate_occupancy_variability(
        building_type
    )

    ventilation_requirement = generate_ventilation_requirement(
        building_type
    )

    recommended_hvac = recommend_hvac(
        building_type,
        area_sqft,
        floors,
        occupancy,
        operating_hours,
        building_age,
        budget_level,
        insulation,
        glass_ratio,
        climate_zone,
        ceiling_height,
        occupancy_variability,
        ventilation_requirement
    )


    row = {

        "building_type": building_type,
        "climate_zone": climate_zone,
        "budget_level": budget_level,

        "area_sqft": area_sqft,
        "floors": floors,
        "ceiling_height": ceiling_height,

        "occupancy": occupancy,
        "operating_hours": operating_hours,
        "building_age": building_age,

        "outdoor_temp": round(outdoor_temp, 2),
        "humidity": round(humidity, 2),

        "insulation": insulation,
        "glass_ratio": glass_ratio,

        "recommended_hvac": recommended_hvac
    }

    dataset.append(row)

df = pd.DataFrame(dataset)

for col in df.columns:
    if col == "recommended_hvac":
        continue
    mask = np.random.rand(len(df)) < 0.02
    df.loc[mask, col] = np.nan

df.to_csv(PROJECT_ROOT / "data/raw/hvac_training_dataset.csv", index=False)

print("\nDataset Shape:", df.shape)

print("\nHVAC Distribution:")
print(df["recommended_hvac"].value_counts())