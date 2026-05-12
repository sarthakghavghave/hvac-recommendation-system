from pydantic import BaseModel
from typing import Optional


class HVACInputSchema(BaseModel):

    building_type: Optional[str] = None
    climate_zone: Optional[str] = None
    budget_level: Optional[str] = None

    area_sqft: Optional[float] = None
    floors: Optional[int] = None
    ceiling_height: Optional[float] = None

    occupancy: Optional[int] = None
    operating_hours: Optional[int] = None
    building_age: Optional[int] = None

    outdoor_temp: Optional[float] = None
    humidity: Optional[float] = None

    insulation: Optional[str] = None
    glass_ratio: Optional[str] = None