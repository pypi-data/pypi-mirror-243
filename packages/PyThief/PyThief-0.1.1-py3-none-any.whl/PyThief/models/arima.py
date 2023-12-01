from darts.models.forecasting.auto_arima import AutoARIMA
from darts.timeseries import TimeSeries
from PyThief.models.base_model import BaseModel


class ArimaModel(BaseModel):
    model = "arima"

    def __init__(self, seasonal_period=24):
        self.seasonal_period = seasonal_period
        self.model_obj = None
        self.fitted = None

    def fit(self, y, key):
        y = y.to_frame().reset_index()
        y = TimeSeries.from_dataframe(
            y, time_col="period", value_cols="y", freq=f"{key}M"
        )
        if len(y) >= 3 * self.seasonal_period and self.seasonal_period == 12:
            m = self.seasonal_period
        else:
            m = 0
        AutoARIMA.min_train_series_length = 3
        self.model_obj = AutoARIMA(
            m=m,
            seasonal=m,
            error_action="warn",
            trace=False,
            supress_warnings=True,
            stepwise=True,
            random_state=20,
            n_fits=50,
        )
        fitted = self.model_obj.fit(y)
        self.fitted = fitted
        return fitted.model.predict_in_sample()

    def predict(self, forecast_horizon):
        predict = self.fitted.predict(forecast_horizon)
        forecasts = predict.pd_series()
        forecasts_values = forecasts.values
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
    model = ArimaModel(12)
    fitted_values = model.fit(y, 1)
    predictions = model.predict(24)
    plt.plot(np.append(fitted_values, predictions), label="arima")
    plt.legend()
