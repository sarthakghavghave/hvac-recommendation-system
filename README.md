# HVAC Recommendation System

## Problem Statement
Wrong HVAC sizing leads to energy inefficiency and poor customer satisfaction.

## Solution
AI-powered HVAC recommendation assistant using:
- Synthetic data generation
- ML recommendation engine
- Prompt-engineered explanations

## Features
- HVAC recommendation
- Capacity estimation
- Energy optimization suggestions
- Explainable AI outputs

## Tech Stack
- Python
- sklearn
- numpy
- pandas
- Streamlit

## Project Architecture
hvac-recommendation-system/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── hvac_synthetic_dataset.csv
│   │
│   └── processed/
|
│
├── notebooks/
│   ├── 01_data_generation.ipynb
│   └── 02_eda.ipynb
|
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/
│   │   └── generate_dataset.py
│   │
│   ├── models/
|   |   └── train_model.py
|   |
│   └── utils/
│       └── config.py
│
├── app/
│   ├── app.py
│   └── pages/
│       ├── 1_Recommendation.py
│       └── 2_Energy_Insights.py
│
├── models/
|   └── hvac_classifier.pkl
│
├── figures/
│
└── tests/
    ├── test_data.py
    ├── test_model.py
    └── test_recommendation.py

## Business Impact
- Faster consultation
- Improved sizing accuracy
- Better conversion rates

## Future Scope
- IoT integration
- Real-time optimization
- Predictive maintenance