import pandas as pd
from dash import Output, Input
from dash import dash_table

from .utils_table import format_sj_bs_df, format_sj_is_df, SectorAnalyser
from .fig import df2data_table, df2plotly_fig, plot_stock_sector_fig

from .utils_graph import FsStockAnalyser
from .fig import draw_fundamental_graph

info_df = pd.read_parquet('./../data/preproc_data/market_data/info_df.parquet')

cfs_sj_bs_fundamental_table_df = pd.read_parquet(
    './../data/integrated_data/financial_statement/cfs_sj_bs_fundamental_table_df.parquet')
cfs_sj_is_fundamental_table_df = pd.read_parquet(
    './../data/integrated_data/financial_statement/cfs_sj_is_fundamental_table_df.parquet')
cfs_fs_df = pd.read_parquet(
    './../data/integrated_data/financial_statement/cfs_fs_df.parquet'
)


def register_fs_table_callback(app):
    @app.callback(
        [
            Output("BS-table", "figure"),
            Output("IS-table", "figure"),
            Output("stock-sector-chart", "figure"),
        ],
        Input("fs-table-dropdown", "value")
    )
    def update_fs_table(selected_stock_nm):
        selected_stock_code = info_df[info_df['stock_name'] == selected_stock_nm]['stock_code'].iloc[0]
        sector_name = info_df[info_df['stock_name'] == selected_stock_nm]['sector'].iloc[0]

        main_bs = format_sj_bs_df(cfs_sj_bs_fundamental_table_df, selected_stock_code)
        bs_table = df2plotly_fig(main_bs)

        main_is = format_sj_is_df(cfs_sj_is_fundamental_table_df, selected_stock_code)
        is_table = df2plotly_fig(main_is)

        sector_analyser = SectorAnalyser(cfs_sj_bs_fundamental_table_df, cfs_sj_is_fundamental_table_df)
        stock_sector_df = sector_analyser(selected_stock_code)
        fig = plot_stock_sector_fig(stock_sector_df, selected_stock_nm, sector_name)
        return [bs_table, is_table, fig]


def register_fs_graph_callback(app):
    @app.callback(
        [
            Output("equity-graph", "figure"),
            Output("profit-graph", "figure"),
        ],
        Input("fs-graph-dropdown", "value")
    )
    def update_fs_graph(selected_stock_nm):
        selected_stock_code = info_df[info_df['stock_name'] == selected_stock_nm]['stock_code'].iloc[0]
        fs_stock_analyser = FsStockAnalyser(cfs_fs_df)
        
        fs_analysis_df = fs_stock_analyser(selected_stock_code)
        _fs_analysis_df = fs_analysis_df.iloc[0, :]
        title = _fs_analysis_df['name'] + '-' + _fs_analysis_df['sector']

        equity_fig = draw_fundamental_graph(fs_analysis_df, title, 'equity_market', 'equity_intrinsic')
        profit_fit = draw_fundamental_graph(fs_analysis_df, title, 'profit_market', 'profit_intrinsic')
        return [equity_fig, profit_fit]
