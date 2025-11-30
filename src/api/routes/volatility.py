from fastapi import APIRouter, HTTPException
from typing import Optional
from ..schemas.models import VolatilityRequest, VolatilityResponse

router = APIRouter()


@router.post("/volatility", response_model=VolatilityResponse)
async def calculate_volatility(request: VolatilityRequest):
    try:
        return {
            "symbol": request.symbol,
            "volatility": [],
            "model": request.model,
            "window": request.window
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/volatility/{symbol}")
async def get_volatility(
    symbol: str,
    model: Optional[str] = "rolling",
    window: int = 30
):
    try:
        return {
            "symbol": symbol,
            "model": model,
            "window": window,
            "volatility": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
