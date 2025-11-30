from fastapi import APIRouter, HTTPException
from typing import Optional
from ..schemas.models import PredictionRequest, PredictionResponse

router = APIRouter()


@router.post("/predictions", response_model=PredictionResponse)
async def create_prediction(request: PredictionRequest):
    try:
        return {
            "symbol": request.symbol,
            "predictions": [],
            "model": request.model,
            "horizon": request.horizon
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictions/{symbol}")
async def get_predictions(
    symbol: str,
    model: Optional[str] = "arima",
    horizon: int = 30
):
    try:
        return {
            "symbol": symbol,
            "model": model,
            "horizon": horizon,
            "predictions": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
