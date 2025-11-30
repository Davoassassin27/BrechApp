import pytest


@pytest.fixture
def sample_data():
    import pandas as pd
    import numpy as np
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    return pd.Series(100 + np.random.randn(100).cumsum(), index=dates)


@pytest.fixture
def sample_returns():
    import pandas as pd
    import numpy as np
    return pd.Series(np.random.randn(100) * 0.01)
