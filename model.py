# models.py
from __future__ import annotations
from enum import Enum
from datetime import datetime, timedelta, timezone
from typing import Optional
import math, re

from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError

# --- Enum for status -------------------------------------------------------
class JobStatus(str, Enum):
    pending = "pending"
    assigned = "assigned"
    en_route = "en_route"
    completed = "completed"
    cancelled = "cancelled"

# --- Location model -------------------------------------------------------
class Location(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    address: Optional[str] = None

    # forbid extra fields by default (helps catch bad payloads)
    model_config = ConfigDict(extra="forbid")

    @field_validator("lat", "lon")
    @classmethod
    def round_coords(cls, v: float) -> float:
        # small nicety: normalize precision
        return round(v, 6)

# --- Vehicle model --------------------------------------------------------
class Vehicle(BaseModel):
    id: str
    type: str = Field(..., description="bike, car, van, ...")
    capacity_kg: float = Field(..., gt=0)
    license_plate: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

# --- Agent model ----------------------------------------------------------
class Agent(BaseModel):
    id: str
    name: str
    phone: str = Field(..., description="international-ish phone, simple validation")
    email: Optional[str] = None
    vehicle: Optional[Vehicle] = None
    location: Location
    active: bool = True

    # validate assignment if you change attributes later
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        # very simple normalization: strip spaces, dashes, parentheses
        return re.sub(r"[\s\-\(\)]", "", v)

# --- Delivery Task model -------------------------------------------------
class DeliveryTask(BaseModel):
    id: str
    pickup: Location
    dropoff: Location
    weight_kg: float = Field(..., gt=0)
    assigned_to: Optional[str] = None  # agent.id
    status: JobStatus = JobStatus.pending
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    scheduled_for: Optional[datetime] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("scheduled_for")
    @classmethod
    def scheduled_must_be_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is None:
            return v
        if v <= datetime.now(timezone.utc):
            raise ValueError("scheduled_for must be in the future")
        return v

    # --- Business methods (not validation) ---------------------------------
    def distance_km(self) -> float:
        """Haversine distance between pickup and dropoff in kilometers."""
        lat1, lon1 = math.radians(self.pickup.lat), math.radians(self.pickup.lon)
        lat2, lon2 = math.radians(self.dropoff.lat), math.radians(self.dropoff.lon)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        R = 6371.0  # Earth radius in km
        return R * c

    def estimated_time_minutes(self, avg_speed_kmph: float = 40.0) -> int:
        """Estimate minutes to complete this trip given an average speed in km/h."""
        dist = self.distance_km()
        if avg_speed_kmph <= 0:
            raise ValueError("avg_speed_kmph must be positive")
        hours = dist / avg_speed_kmph
        minutes = int(hours * 60)
        # add small fixed overhead for stops
        return max(1, minutes + 5)

    # def is_overdue(self) -> bool:
    #     """Check if the task is overdue based on scheduled_for."""
    #     if self.scheduled_for is None:
    #         return False