from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from predict import predict_data
from data import load_data
from logger_config import get_logger


x, y, target_names = load_data()
app = FastAPI()
api_logger = get_logger("api", "health_api.log")

class HealthData(BaseModel):
    bmi: float
    cholesterol: float
    blood_pressure: float

class HealthResponse(BaseModel):
    response: int

class HealthNameResponse(BaseModel):
    status: str

@app.post("/predict_name", response_model=HealthNameResponse)
async def predict_health_name(health_features: HealthData):

    api_logger.info(f"PredictRequest: bmi={health_features.bmi}, "
                    f"chol={health_features.cholesterol}, bp={health_features.blood_pressure}")

    try:
        features = [[health_features.bmi,
                     health_features.cholesterol,
                     health_features.blood_pressure]]
        prediction = predict_data(features)
        status_name = target_names[int(prediction[0])]

        api_logger.info(f"PredictResponse: status_name={status_name}")

        return HealthNameResponse(status=status_name)

    except Exception as e:
        api_logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
