from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BuildingType(str, Enum):
    Residential = "Residential"
    Office = "Office"
    Retail = "Retail"
    Hospital = "Hospital"
    Industrial = "Industrial"


class ClimateZone(str, Enum):
    Hot = "Hot"
    Warm = "Warm"
    Cold = "Cold"
    Humid = "Humid"


class BudgetLevel(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class Insulation(str, Enum):
    Poor = "Poor"
    Average = "Average"
    Good = "Good"
    Excellent = "Excellent"


class GlassRatio(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class HVACInputSchema(BaseModel):

    building_type: Optional[BuildingType] = None
    climate_zone: Optional[ClimateZone] = None
    budget_level: Optional[BudgetLevel] = None

    area_sqft: Optional[float] = None
    floors: Optional[int] = None
    ceiling_height: Optional[float] = None

    occupancy: Optional[int] = None
    operating_hours: Optional[int] = None
    building_age: Optional[int] = None

    outdoor_temp: Optional[float] = None
    humidity: Optional[float] = None

    insulation: Optional[Insulation] = None
    glass_ratio: Optional[GlassRatio] = None