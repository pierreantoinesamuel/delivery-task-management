import pytest
from pydantic import ValidationError
from model import DeliveryTask

def test_invalid_weight():
    bad = {"id":"t", "pickup": {"lat":0, "lon":0}, "dropoff":{"lat":1,"lon":1}, "weight_kg": -1}
    with pytest.raises(ValidationError):
        DeliveryTask.model_validate(bad)

def test_distance_positive():
    t = DeliveryTask.model_validate({
        "id":"t2",
        "pickup": {"lat":48.8566,"lon":2.3522},
        "dropoff":{"lat":51.5074,"lon":-0.1278},
        "weight_kg": 3.0
    })
    assert t.distance_km() > 0
