import pickle
from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_DIR / "data"/ "raw" / "hvac_training_dataset.csv"
MODEL_DIR = ROOT_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "hvac_rf_model.pkl"

df = pd.read_csv(DATA_PATH)

TARGET = "recommended_hvac"

FEATURES = [

    "building_type",
    "climate_zone",
    "budget_level",

    "area_sqft",
    "floors",
    "ceiling_height",

    "occupancy",
    "operating_hours",
    "building_age",

    "outdoor_temp",
    "humidity",

    "insulation",
    "glass_ratio"
]

X = df[FEATURES]
y = df[TARGET]

categorical_features = [

    "building_type",
    "climate_zone",
    "budget_level",

    "insulation",
    "glass_ratio"
]

numeric_features = [

    "area_sqft",
    "floors",
    "ceiling_height",

    "occupancy",
    "operating_hours",
    "building_age",

    "outdoor_temp",
    "humidity"
]

numeric_pipeline = Pipeline([
    ("imputer",SimpleImputer(strategy="median")),
    ("scaler",StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer",SimpleImputer(strategy="most_frequent")),
    ("encoder",OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num",numeric_pipeline,numeric_features),
    ("cat",categorical_pipeline,categorical_features)
])

rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocessor",preprocessor),
    ("classifier", rf)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("\nTraining model...\n")

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test,y_pred)

print(f"\nAccuracy: {accuracy:.4f}\n")

print(classification_report(y_test,y_pred))

with open(MODEL_PATH, "wb") as file:
    pickle.dump(pipeline,file)

print(f"\nModel saved at:\n{MODEL_PATH}")