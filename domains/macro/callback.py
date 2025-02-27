import pandas as pd
from dash import Output, Input
from domains.macro.fig import draw_macro_graph

macro_df = pd.read_parquet('./../data/integrated_data/macro_data/macro_df.parquet')

def register_macro_callback(app):
    @app.callback(
        Output("macro-indicator-chart", "figure"),
        Input("macro-indicator-dropdown-1", "value"),
        Input("macro-indicator-dropdown-2", "value")
    )
    def update_macro_graph(indicator_1, indicator_2):
        return draw_macro_graph(macro_df, indicator_1, indicator_2)