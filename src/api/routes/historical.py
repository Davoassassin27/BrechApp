from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

router = APIRouter()


@router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = Query(default="1d", regex="^(1m|5m|15m|30m|1h|1d|1wk|1mo)$")
):
    try:
        return {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval,
            "data": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historical/{symbol}/stats")
async def get_historical_stats(symbol: str):
    try:
        return {
            "symbol": symbol,
            "mean": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0,
            "count": 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
