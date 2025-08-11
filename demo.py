from datetime import datetime, timedelta, timezone
from model import Location, DeliveryTask
from pydantic import ValidationError

# Sample pickup and dropoff
pickup = {"lat": 48.8566, "lon": 2.3522, "address": "Paris center"}       # Paris
dropoff = {"lat": 48.864716, "lon": 2.349014, "address": "Near Louvre"}  # Louvre

# Task data
task_payload = {
    "id": "task_001",
    "pickup": pickup,
    "dropoff": dropoff,
    "weight_kg": 2.5,
    "scheduled_for": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
}

try:
    # Create and validate the task
    task = DeliveryTask.model_validate(task_payload)  # v2 method
    print("Task created:", task.model_dump())         # dictionary output
    print("Distance (km):", round(task.distance_km(), 2))
    print("ETA minutes:", task.estimated_time_minutes(avg_speed_kmph=12))
except ValidationError as e:
    print("Validation failed:", e)
