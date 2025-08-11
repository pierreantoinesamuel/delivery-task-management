# demo_folium.py
from datetime import datetime, timedelta, timezone
import folium
from model import DeliveryTask
from pydantic import ValidationError

def interpolate_coords(a, b, n):
    """Return n points including endpoints between a=(lat,lon) and b=(lat,lon)."""
    lat1, lon1 = a
    lat2, lon2 = b
    return [(lat1 + (lat2 - lat1) * i / (n - 1),
             lon1 + (lon2 - lon1) * i / (n - 1))
            for i in range(n)]

# --- here to create or modify a validated DeliveryTask (uses your models.py DeliveryTask) ---
pickup = {"lat": 48.8566, "lon": 2.3522, "address": "Paris center"}
dropoff = {"lat": 48.864716, "lon": 2.349014, "address": "Near Louvre"}

task_payload = {
    "id": "task_001",
    "pickup": pickup,
    "dropoff": dropoff,
    "weight_kg": 2.5,
    "scheduled_for": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
}

try:
    task = DeliveryTask.model_validate(task_payload)
except ValidationError as e:
    print("Validation failed:", e)
    raise SystemExit(1)

start = (task.pickup.lat, task.pickup.lon)
end = (task.dropoff.lat, task.dropoff.lon)

# create map centered between start and end
center = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
m = folium.Map(location=center, zoom_start=15)

# markers for pickup / dropoff
folium.Marker([start[0], start[1]], popup="Pickup", tooltip="Pickup").add_to(m)
folium.Marker([end[0], end[1]], popup="Dropoff", tooltip="Dropoff").add_to(m)

# straight-line polyline
folium.PolyLine(locations=[[start[0], start[1]], [end[0], end[1]]],
                color="blue", weight=3, opacity=0.8).add_to(m)

# create 6 simple "step" markers by interpolation
for i, (lat, lon) in enumerate(interpolate_coords(start, end, n=6), start=1):
    folium.CircleMarker([lat, lon], radius=4,
                        popup=f"Step {i}",
                        tooltip=f"Step {i}").add_to(m)

out_file = "route_folium.html"
m.save(out_file)
print(f"Saved map to {out_file}")
print("Distance (km):", round(task.distance_km(), 2))
print("ETA minutes:", task.estimated_time_minutes(avg_speed_kmph=12))
