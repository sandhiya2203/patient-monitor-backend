from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from contextlib import asynccontextmanager

from consumer import patient_data, start_consumer



@asynccontextmanager
async def lifespan(app: FastAPI):

    start_consumer()

    yield



app = FastAPI(
    lifespan=lifespan
)



# CSS and JS folder
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)



# HTML file inside templates

@app.get("/")
def home():

    return FileResponse(
        "templates/index.html"
    )



@app.get("/data")
def get_data():

    return patient_data



@app.get("/patient")
def patient():

    return patient_data
@app.post("/update")
def update(data: dict):

    patient_data["heart_rate"] = data["heart_rate"]
    patient_data["systolic_bp"] = data["systolic_bp"]
    patient_data["diastolic_bp"] = data["diastolic_bp"]
    patient_data["spo2"] = data["spo2"]

    return {
        "status": "updated",
        "data": patient_data
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000
    )

