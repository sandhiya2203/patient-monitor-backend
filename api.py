from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


patient_data = {
    "status": "Waiting",
    "heart_rate": 0,
    "spo2": 0,
    "systolic_bp": 0,
    "diastolic_bp": 0,
    "last_update": "No Data"
}


# Store last communication time
last_update_seconds = time.time()


@app.post("/update")
def update_patient(data: dict):

    global patient_data, last_update_seconds

    # Receive data from consumer
    patient_data = data

    # Update heartbeat time
    last_update_seconds = time.time()

    # Store last received time
    patient_data["last_update"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "message": "Updated"
    }



@app.get("/patient")
def get_patient():

    global patient_data, last_update_seconds


    # No data received for 5 seconds
    if time.time() - last_update_seconds > 5:

        patient_data["status"] = "Disconnected"


    return patient_data
