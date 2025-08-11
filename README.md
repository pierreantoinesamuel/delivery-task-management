#  AI Coding Agents

## Project Overview
- This is a Python project for delivery task management, using FastAPI for the API layer and Pydantic for data validation and business logic.
- The codebase is organized as a single-folder app with models, API, demo scripts, and tests.

## Key Components
- `model.py`: Defines core data models (`Location`, `Vehicle`, `Agent`, `DeliveryTask`, `JobStatus`) using Pydantic. Includes business logic (distance, ETA calculations) and strict validation (e.g., timezone-aware datetimes, no extra fields).
- `main.py`: FastAPI app exposing a `/tasks` POST endpoint. Accepts and returns `DeliveryTask` objects. No database or persistence layer is present.
- `demo.py`, `route_folium.py`: Standalone scripts for validating models and visualizing delivery routes. Use timezone-aware datetimes (`datetime.now(timezone.utc)`).
- `test_models.py`: Pytest-based unit tests for model validation and business logic.

## Developer Workflows
- **Run API server:**
  ```powershell
  uvicorn main:app --reload
  ```
- **Run tests:**
  ```powershell
  pytest test_models.py
  ```
- **Run demo scripts:**
  ```powershell
  python demo.py
  python route_folium.py
  ```
- **View API docs:**
  Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## Project-Specific Conventions
- All datetimes must be timezone-aware (`datetime.now(timezone.utc)`), both in models and payloads.
- Pydantic models use `extra="forbid"` to reject unknown fields.
- Validation logic (e.g., `scheduled_for` must be in the future) is enforced via Pydantic `field_validator`.
- Business logic (distance, ETA) is implemented as methods on models, not in the API layer.
- No database or async patterns are present; persistence is not implemented.

## External Dependencies
- `fastapi`, `uvicorn` for API
- `pydantic` for models/validation
- `pytest` for testing
- `folium` for route visualization (see `route_folium.py`)

## Examples
- See `demo.py` for model instantiation and validation patterns.
- See `test_models.py` for test structure and validation error handling.
- See `route_folium.py` for integration with external libraries (folium) and model usage.

---

For questions about unclear conventions or missing documentation, please provide feedback to improve these instructions.
