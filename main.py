# main.py
from fastapi import FastAPI
from model import DeliveryTask

app = FastAPI()

@app.post("/tasks", response_model=DeliveryTask)
def create_task(task: DeliveryTask):
    # Log the received task as JSON
    print(f"Received task: {task.model_dump_json()}")
    # Here you would typically save the task to a database
    # In a real app you'd persist the task and return the saved record
    return task
