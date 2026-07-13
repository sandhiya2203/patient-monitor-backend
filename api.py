from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

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
    "diastolic_bp": 0
}


# Store last communication time
last_update_time = time.time()


@app.post("/update")
def update_patient(data: dict):

    global patient_data, last_update_time

    patient_data = data

    # update heartbeat time
    last_update_time = time.time()

    return {"message": "Updated"}



@app.get("/patient")
def get_patient():

    global patient_data, last_update_time

    # If no data received for 5 seconds
    if time.time() - last_update_time > 5:

        patient_data["status"] = "Disconnected"


    return patient_data
