from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

info_df = pd.read_parquet('./../data/preproc_data/market_data/info_df.parquet')
name_sector_dict = info_df.set_index('stock_name')['sector'].to_dict()

fs_table_layout = dbc.Container([
    html.H2("재무제표 테이블", className="text-center"),
    dcc.Dropdown(
        id="fs-table-dropdown",
        options=[{"label": ticker+'-'+name_sector_dict[ticker], "value": ticker} for ticker in info_df['stock_name'].unique()],
        value=info_df["stock_name"].unique()[0],
        clearable=False
    ),
    
    html.Br(),  # 간격 추가
    html.H3("재무제표", className="text-center"),
    dcc.Graph(id='BS-table'),
    
    html.H3("손익", className="text-center"),
    dcc.Graph(id='IS-table'),
    
    html.H3("종목 vs 섹터", className="text-center"),
    dcc.Graph(id='stock-sector-chart'),
    
    html.Br(),
    html.Br(),
    html.Br(),
    
])

fs_graph_layout = dbc.Container([
    html.H2("재무제표 그래프", className="text-center"),
    dcc.Dropdown(
        id="fs-graph-dropdown",
        options=[{"label": ticker+'-'+name_sector_dict[ticker], "value": ticker} for ticker in info_df['stock_name'].unique()],
        value=info_df["stock_name"].unique()[0],
        clearable=False
    ),
    
    html.Br(),  # 간격 추가
    html.H3("자산 평가", className="text-center"),
    dcc.Graph(id='equity-graph'),
    
    html.H3("수익 평가", className="text-center"),
    dcc.Graph(id='profit-graph'),
])