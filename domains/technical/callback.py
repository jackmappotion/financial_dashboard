import pandas as pd
from dash import Output, Input

from domains.technical.utils import replace_zero, get_recent_n_days
from domains.technical.utils import LowessSmoother, SplineSmoother
from domains.technical.fig import plot_candle_chart, plot_candle_with_smooth

ohlcv_df = pd.read_parquet('./../data/preproc_data/market_data/ohlcv_df.parquet')
info_df = pd.read_parquet('./../data/preproc_data/market_data/info_df.parquet')


def register_price_callback(app):
    @app.callback(
        [
            Output("price-chart-60", "figure"),
            Output("price-chart-120", "figure"),
            Output("price-chart-365", "figure"),
            Output("price-chart-tot", "figure"),
        ],
        Input("price-dropdown", "value")
    )
    def update_price_chart(selected_stock_nm):
        selected_stock_code = info_df[info_df['stock_name'] == selected_stock_nm]['stock_code'].iloc[0]
        _ohlcv_df = ohlcv_df[ohlcv_df["stock_code"] == selected_stock_code].copy()
        
        _ohlcv_df = replace_zero(_ohlcv_df)
        _ohlcv_df_365 = get_recent_n_days(_ohlcv_df, 365)
        _ohlcv_df_120 = get_recent_n_days(_ohlcv_df, 120)
        _ohlcv_df_60 = get_recent_n_days(_ohlcv_df, 60)

        _fig_60 = plot_candle_chart(_ohlcv_df_60)
        _fig_120 = plot_candle_chart(_ohlcv_df_120)
        _fig_365 = plot_candle_chart(_ohlcv_df_365)
        _fig = plot_candle_chart(_ohlcv_df)

        return [_fig_60, _fig_120, _fig_365, _fig]


def register_lowess_callback(app):
    @app.callback(
        [
            Output("lowess-chart-60", "figure"),
            Output("lowess-chart-120", "figure"),
            Output("lowess-chart-365", "figure"),
            Output("lowess-chart-tot", "figure"),
        ],
        Input("lowess-dropdown", "value")
    )
    def update_lowess_chart(selected_stock_nm):
        selected_stock_code = info_df[info_df['stock_name'] == selected_stock_nm]['stock_code'].iloc[0]
        _ohlcv_df = ohlcv_df[ohlcv_df["stock_code"] == selected_stock_code].copy()

        _ohlcv_df = replace_zero(_ohlcv_df)
        _ohlcv_df_365 = get_recent_n_days(_ohlcv_df, 365)
        _ohlcv_df_120 = get_recent_n_days(_ohlcv_df, 120)
        _ohlcv_df_60 = get_recent_n_days(_ohlcv_df, 60)

        _fig_60 = plot_candle_with_smooth(_ohlcv_df_60, LowessSmoother(_ohlcv_df_60['close'])())
        _fig_120 = plot_candle_with_smooth(_ohlcv_df_120, LowessSmoother(_ohlcv_df_120['close'])())
        _fig_365 = plot_candle_with_smooth(_ohlcv_df_365, LowessSmoother(_ohlcv_df_365['close'])())
        _fig = plot_candle_with_smooth(_ohlcv_df, LowessSmoother(_ohlcv_df['close'])())

        return [_fig_60, _fig_120, _fig_365, _fig]

def register_spline_callback(app):
    @app.callback(
        [
            Output("spline-chart-60", "figure"),
            Output("spline-chart-120", "figure"),
            Output("spline-chart-365", "figure"),
            Output("spline-chart-tot", "figure"),
        ],
        Input("spline-dropdown", "value")
    )
    def update_spline_chart(selected_stock_nm):
        selected_stock_code = info_df[info_df['stock_name'] == selected_stock_nm]['stock_code'].iloc[0]
        _ohlcv_df = ohlcv_df[ohlcv_df["stock_code"] == selected_stock_code].copy()

        _ohlcv_df = replace_zero(_ohlcv_df)
        _ohlcv_df_365 = get_recent_n_days(_ohlcv_df, 365)
        _ohlcv_df_120 = get_recent_n_days(_ohlcv_df, 120)
        _ohlcv_df_60 = get_recent_n_days(_ohlcv_df, 60)

        _fig_60 = plot_candle_with_smooth(_ohlcv_df_60, SplineSmoother(_ohlcv_df_60['close'])())
        _fig_120 = plot_candle_with_smooth(_ohlcv_df_120, SplineSmoother(_ohlcv_df_120['close'])())
        _fig_365 = plot_candle_with_smooth(_ohlcv_df_365, SplineSmoother(_ohlcv_df_365['close'])())
        _fig = plot_candle_with_smooth(_ohlcv_df, SplineSmoother(_ohlcv_df['close'])())

        return [_fig_60, _fig_120, _fig_365, _fig]
