import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from .time_series import ARIMAModel, ProphetModel
from .volatility import GARCHModel, RollingVolatility


class Predictor:
    def __init__(self):
        self.models = {}
        self.fitted_models = {}
    
    def add_model(self, name: str, model):
        self.models[name] = model
        return self
    
    def fit(self, data: pd.Series, model_name: Optional[str] = None):
        if model_name:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            self.models[model_name].fit(data)
            self.fitted_models[model_name] = self.models[model_name]
        else:
            for name, model in self.models.items():
                model.fit(data)
                self.fitted_models[name] = model
        return self
    
    def predict(self, model_name: str, **kwargs) -> Any:
        if model_name not in self.fitted_models:
            raise ValueError(f"Model {model_name} not fitted")
        return self.fitted_models[model_name].predict(**kwargs)
    
    def predict_all(self, **kwargs) -> Dict[str, Any]:
        predictions = {}
        for name, model in self.fitted_models.items():
            try:
                predictions[name] = model.predict(**kwargs)
            except Exception as e:
                predictions[name] = {'error': str(e)}
        return predictions
    
    def get_model(self, name: str):
        return self.fitted_models.get(name)
    
    def list_models(self):
        return list(self.models.keys())
    
    def list_fitted_models(self):
        return list(self.fitted_models.keys())
