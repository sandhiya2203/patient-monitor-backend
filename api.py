from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.post("/update")
def update_patient(data: dict):
    global patient_data
    patient_data = data
    return {"message": "Updated"}


@app.get("/patient")
def get_patient():
    return patient_data
