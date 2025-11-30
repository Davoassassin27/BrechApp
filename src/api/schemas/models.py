from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PredictionRequest(BaseModel):
    symbol: str = Field(..., description="Cryptocurrency symbol")
    model: str = Field(default="arima", description="Model to use for prediction")
    horizon: int = Field(default=30, description="Prediction horizon in days")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC-USD",
                "model": "arima",
                "horizon": 30
            }
        }


class PredictionResponse(BaseModel):
    symbol: str
    predictions: List[dict]
    model: str
    horizon: int


class VolatilityRequest(BaseModel):
    symbol: str = Field(..., description="Cryptocurrency symbol")
    model: str = Field(default="rolling", description="Volatility model")
    window: int = Field(default=30, description="Window size for rolling calculations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "BTC-USD",
                "model": "rolling",
                "window": 30
            }
        }


class VolatilityResponse(BaseModel):
    symbol: str
    volatility: List[dict]
    model: str
    window: int
