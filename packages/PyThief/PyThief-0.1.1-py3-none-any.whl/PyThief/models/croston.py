from statsforecast.models import CrostonClassic
from statsforecast.models import CrostonOptimized
from statsforecast.models import CrostonSBA
from PyThief.models.base_model import BaseModel


class CrostonModel(BaseModel):
    model = "croston"

    def __init__(self, version="classic"):
        self.version = version
        self.model_obj = None
        self.fitted = None

    def fit(self, y):
        if self.version == "classic":
            self.model_obj = CrostonClassic()
        elif self.version == "optimized":
            self.model_obj = CrostonOptimized()
        elif self.version == "sba":
            self.model_obj = CrostonSBA()
        fitted = self.model_obj.fit(y.to_numpy())
        self.fitted = fitted
        return y.to_numpy()

    def predict(self, forecast_horizon):
        predict = self.fitted.predict(forecast_horizon)
        forecasts_values = predict["mean"]
        forecasts_values[forecasts_values < 0] = 0
        return forecasts_values


#%%
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    y = [
        69,
        2777,
        17356,
        13972,
        420,
        6774,
        8337,
        7956,
        6430,
        4203,
        5603,
        13586,
        29564,
        17635,
        19174,
        21360,
        4413,
        9010,
        711,
        29031,
        15225,
        13870,
        45360,
        20360,
        75956,
        28474,
        22928,
        77955,
        24161,
        3780,
        15897,
        16898,
        4222,
        14006,
        24484,
        48973,
        21222,
        21322,
        11649,
        9797,
        25350,
        68135,
        7336,
        39371,
        21148,
        59876,
        172433,
        26669,
        15614,
        37894,
        22022,
    ]
    periods = [
        "2017-12-31T00:00:00.000+0000",
        "2018-01-31T00:00:00.000+0000",
        "2018-02-28T00:00:00.000+0000",
        "2018-03-31T00:00:00.000+0000",
        "2018-04-30T00:00:00.000+0000",
        "2018-05-31T00:00:00.000+0000",
        "2018-06-30T00:00:00.000+0000",
        "2018-07-31T00:00:00.000+0000",
        "2018-08-31T00:00:00.000+0000",
        "2018-09-30T00:00:00.000+0000",
        "2018-10-31T00:00:00.000+0000",
        "2018-11-30T00:00:00.000+0000",
        "2018-12-31T00:00:00.000+0000",
        "2019-01-31T00:00:00.000+0000",
        "2019-02-28T00:00:00.000+0000",
        "2019-03-31T00:00:00.000+0000",
        "2019-04-30T00:00:00.000+0000",
        "2019-05-31T00:00:00.000+0000",
        "2019-06-30T00:00:00.000+0000",
        "2019-07-31T00:00:00.000+0000",
        "2019-08-31T00:00:00.000+0000",
        "2019-09-30T00:00:00.000+0000",
        "2019-10-31T00:00:00.000+0000",
        "2019-11-30T00:00:00.000+0000",
        "2019-12-31T00:00:00.000+0000",
        "2020-01-31T00:00:00.000+0000",
        "2020-02-29T00:00:00.000+0000",
        "2020-03-31T00:00:00.000+0000",
        "2020-04-30T00:00:00.000+0000",
        "2020-05-31T00:00:00.000+0000",
        "2020-06-30T00:00:00.000+0000",
        "2020-07-31T00:00:00.000+0000",
        "2020-08-31T00:00:00.000+0000",
        "2020-09-30T00:00:00.000+0000",
        "2020-10-31T00:00:00.000+0000",
        "2020-11-30T00:00:00.000+0000",
        "2020-12-31T00:00:00.000+0000",
        "2021-01-31T00:00:00.000+0000",
        "2021-02-28T00:00:00.000+0000",
        "2021-03-31T00:00:00.000+0000",
        "2021-04-30T00:00:00.000+0000",
        "2021-05-31T00:00:00.000+0000",
        "2021-06-30T00:00:00.000+0000",
        "2021-07-31T00:00:00.000+0000",
        "2021-08-31T00:00:00.000+0000",
        "2021-09-30T00:00:00.000+0000",
        "2021-10-31T00:00:00.000+0000",
        "2021-11-30T00:00:00.000+0000",
        "2021-12-31T00:00:00.000+0000",
        "2022-01-31T00:00:00.000+0000",
        "2022-02-28T00:00:00.000+0000",
    ]
    data = {"period": periods, "y": y}
    y = pd.DataFrame(data)
    y = y.set_index("period")["y"]
    model_o = CrostonModel("optimized")
    fitted_values_o = model_o.fit(y)
    predictions_o = model_o.predict(24)
    model_c = CrostonModel("classic")
    fitted_values_c = model_c.fit(y)
    predictions_c = model_c.predict(24)
    model_s = CrostonModel("sba")
    fitted_values_s = model_s.fit(y)
    predictions_s = model_s.predict(24)
    plt.plot(np.append(y, predictions_o), label="croston_o")
    plt.plot(np.append(y, predictions_c), label="croston_c")
    plt.plot(np.append(y, predictions_s), label="croston_s")
    plt.legend()
