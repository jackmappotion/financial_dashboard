import pandas as pd
import numpy as np
import datetime as dt

from statsmodels.nonparametric.smoothers_lowess import lowess
from sklearn.preprocessing import MinMaxScaler
from scipy.interpolate import UnivariateSpline

def replace_zero(ohlcv_df):
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    ohlcv_df.loc[:,numeric_cols] = ohlcv_df.loc[:,numeric_cols].replace(0, np.NaN).bfill().ffill()
    return ohlcv_df


def get_recent_n_days(ohlcv_df, n):
    max_date = ohlcv_df['date'].max()
    threshold = max_date - dt.timedelta(days=n)
    _ohlcv_df = ohlcv_df[threshold <= ohlcv_df['date']]
    return _ohlcv_df

class LowessSmoother:
    def __init__(self, series):
        self.series = series

    def auto_frac(self):
        n = len(self.series)
        return min(0.2, max(0.025, 50 / n))

    @staticmethod
    def smooth(series, frac):
        ''' 0 < frac < 1 '''

        x = np.arange(1, len(series) + 1)
        y = series.to_numpy()

        result = lowess(y, x, frac=frac)

        smoothed_arr = result[:, 1]
        smoothed_series = pd.Series(smoothed_arr, index=series.index, name=series.name)
        return smoothed_series

    def __call__(self, ticks=None, frac=None):
        series = self.series.copy()
        if ticks:
            series = series.tail(ticks)
        if frac is None:
            frac = self.auto_frac()
        smoothed_series = self.smooth(series, frac)
        return smoothed_series
    

class SplineSmoother:
    def __init__(self, series):
        self.series = series

    def auto_s(self):
        n = len(self.series)
        return max(1, min(1000, n / 200))

    @staticmethod
    def smooth(series, s):
        ''''''

        x = np.arange(1, len(series) + 1)
        y = series.to_numpy().reshape(-1, 1)

        mms_y = MinMaxScaler()
        scaled_y = mms_y.fit_transform(y).flatten()

        spline = UnivariateSpline(x, scaled_y, s=s)
        scaled_smoothed_y = spline(x)
        smoothed_arr = mms_y.inverse_transform(scaled_smoothed_y.reshape(-1, 1)).flatten()
        smoothed_series = pd.Series(smoothed_arr, index=series.index, name=series.name)
        return smoothed_series

    def __call__(self, ticks=None, s=None):
        series = self.series.copy()
        if ticks:
            series = series.tail(ticks)
        
        if s is None:
            s = self.auto_s()
        smoothed_series = self.smooth(series, s)
        return smoothed_series
    
class InflectionPoint:
    def __init__(self, series):
        self.series = series

    @staticmethod
    def get_inflection_points(series, window):
        from scipy.signal import argrelextrema

        local_maxima = argrelextrema(series.to_numpy(), np.greater, order=window)[0]
        local_minima = argrelextrema(series.to_numpy(), np.less, order=window)[0]

        inflection_points = sorted(np.concatenate((local_maxima, local_minima)))
        return inflection_points

    def get_points(self, window=10):
        series = self.series.copy()
        points = self.get_inflection_points(series, window)
        return points

    def get_df(self, window=10):
        series = self.series.copy()
        points = self.get_inflection_points(series, window)
        df = series.to_frame().copy()
        df['point'] = 0
        df.loc[df.index[points], 'point'] = 1
        return df