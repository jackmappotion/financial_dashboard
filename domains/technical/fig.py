import plotly.graph_objects as go
from .utils import InflectionPoint

def plot_candle_chart(ohlcv_df):
    fig = go.Figure(data=[go.Candlestick(x=ohlcv_df['date'],
                                         open=ohlcv_df['open'],
                                         high=ohlcv_df['high'],
                                         low=ohlcv_df['low'],
                                         close=ohlcv_df['close'],
                                         increasing=dict(line=dict(color='red')),  # 상승 (빨강)
                                         decreasing=dict(line=dict(color='blue'))  # 하락 (파랑)
                                         )])

    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def plot_candle_with_smooth(ohlcv_df, smoothed_series):
    inflection_df = InflectionPoint(smoothed_series).get_df(30)
    inflection_df.index = ohlcv_df['date']
    _inflection_df = inflection_df[inflection_df['point'] == 1]
    
    fig = go.Figure(data=[go.Candlestick(x=ohlcv_df['date'],
                                         open=ohlcv_df['open'],
                                         high=ohlcv_df['high'],
                                         low=ohlcv_df['low'],
                                         close=ohlcv_df['close'],
                                         name='price',
                                         increasing=dict(line=dict(color='red')),  # 상승 (빨강)
                                         decreasing=dict(line=dict(color='blue'))  # 하락 (파랑)
                                         )])
    fig.add_trace(go.Scatter(x=ohlcv_df['date'], y=smoothed_series,
                             mode="lines",
                             opacity=0.5,
                             line=dict(color="gray", width=20),
                             name="lowess_price",
                             )
                  )
    fig.add_trace(go.Scatter(x=_inflection_df.index, y=_inflection_df['close'],
                         mode="markers",
                         marker=dict(size=30, color='black', symbol='x'),
                         name='inflection_point',
                         opacity=0.5,
                         )
              )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig
