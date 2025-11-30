from fastapi import FastAPI
from .routes import predictions, volatility, historical

app = FastAPI(
    title="BrechApp API",
    description="API for cryptocurrency breach detection and prediction",
    version="1.0.0"
)

app.include_router(predictions.router, prefix="/api/v1", tags=["predictions"])
app.include_router(volatility.router, prefix="/api/v1", tags=["volatility"])
app.include_router(historical.router, prefix="/api/v1", tags=["historical"])


@app.get("/")
async def root():
    return {
        "message": "BrechApp API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
