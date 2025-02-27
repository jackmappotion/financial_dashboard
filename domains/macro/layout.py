from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

macro_df = pd.read_parquet('./../data/integrated_data/macro_data/macro_df.parquet')

macro_layout = dbc.Container([
    html.H2("📊 경제 지표 비교", className="text-center"),

    dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="macro-indicator-dropdown-1",
                options=[{"label": col, "value": col} for col in macro_df.columns if col != "date"],
                value=macro_df.columns[1],
                clearable=False
            ), width=6),

            dbc.Col(dcc.Dropdown(
                id="macro-indicator-dropdown-2",
                options=[{"label": col, "value": col} for col in macro_df.columns if col != "date"],
                value=macro_df.columns[2],
                clearable=False
            ), width=6),
            ]),
    dcc.Graph(id="macro-indicator-chart"),
])
