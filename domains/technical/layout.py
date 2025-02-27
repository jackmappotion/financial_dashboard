from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

info_df = pd.read_parquet('./../data/preproc_data/market_data/info_df.parquet')
name_sector_dict = info_df.set_index('stock_name')['sector'].to_dict()

price_layout = dbc.Container([
    html.H2("💹 가격 데이터", className="text-center"),
    dcc.Dropdown(
        id="price-dropdown",
        options=[{"label": ticker+'-'+name_sector_dict[ticker], "value": ticker} for ticker in info_df['stock_name'].unique()],
        value=info_df["stock_name"].unique()[0],
        clearable=False
    ),
    
    html.Br(),  # 간격 추가

    html.H3("60일 데이터", className="text-center"),
    dcc.Graph(id="price-chart-60"),

    html.H3("120일 데이터", className="text-center"),
    dcc.Graph(id="price-chart-120"),

    html.H3("1년 데이터", className="text-center"),
    dcc.Graph(id="price-chart-365"),

    html.H3("전체 데이터", className="text-center"),
    dcc.Graph(id="price-chart-tot"),
])

lowess_layout = dbc.Container([
    html.H2("💹 LOWESS Analysis 데이터", className="text-center"),
    dcc.Dropdown(
        id="lowess-dropdown",
        options=[{"label": ticker+'-'+name_sector_dict[ticker], "value": ticker} for ticker in info_df['stock_name'].unique()],
        value=info_df["stock_name"].unique()[0],
        clearable=False
    ),
    
    html.Br(),  # 간격 추가

    html.H3("60일 데이터", className="text-center"),
    dcc.Graph(id="lowess-chart-60"),

    html.H3("120일 데이터", className="text-center"),
    dcc.Graph(id="lowess-chart-120"),

    html.H3("1년 데이터", className="text-center"),
    dcc.Graph(id="lowess-chart-365"),

    html.H3("전체 데이터", className="text-center"),
    dcc.Graph(id="lowess-chart-tot"),
])

spline_layout = dbc.Container([
    html.H2("💹 SPLINE Analysis 데이터", className="text-center"),
    dcc.Dropdown(
        id="spline-dropdown",
        options=[{"label": ticker+'-'+name_sector_dict[ticker], "value": ticker} for ticker in info_df['stock_name'].unique()],
        value=info_df["stock_name"].unique()[0],
        clearable=False
    ),
    
    html.Br(),  # 간격 추가

    html.H3("60일 데이터", className="text-center"),
    dcc.Graph(id="spline-chart-60"),

    html.H3("120일 데이터", className="text-center"),
    dcc.Graph(id="spline-chart-120"),

    html.H3("1년 데이터", className="text-center"),
    dcc.Graph(id="spline-chart-365"),

    html.H3("전체 데이터", className="text-center"),
    dcc.Graph(id="spline-chart-tot"),
])
