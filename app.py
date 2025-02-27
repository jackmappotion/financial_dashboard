from dash import Dash, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Index
from index import create_layout

# Layouts
from domains.macro.layout import macro_layout
from domains.technical.layout import price_layout, lowess_layout, spline_layout
# from domains.fundamental.layout import fs_table_layout
from domains.fundamental.layout import fs_table_layout,fs_graph_layout
# from domains.fundamental.layout import (fs_table_layout,fs_graph_layout,fs_indicator_layout)

# Callbacks
from domains.macro.callback import register_macro_callback
from domains.technical.callback import register_price_callback, register_lowess_callback, register_spline_callback
from domains.fundamental.callback import register_fs_table_callback, register_fs_graph_callback

# Dash App Initialize
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_layout()

# Callbacks
## [main]
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    layouts = {
        # Economics
        "/macro": macro_layout,
        
        # Techincals
        "/technical/price": price_layout,
        "/technical/lowess": lowess_layout,
        "/technical/spline": spline_layout,
        
        # # Fundamentals
        "/fundamental/fs_table": fs_table_layout,
        "/fundamental/fs_graph": fs_graph_layout,
        # "/fundamental/fs_indicator": fs_indicator_layout,
    }
    return layouts.get(pathname, html.H4("📌 왼쪽 메뉴에서 페이지를 선택하세요.", className="text-center"))

## [domain]
register_macro_callback(app)

register_price_callback(app)
register_lowess_callback(app)
register_spline_callback(app)

register_fs_table_callback(app)
register_fs_graph_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
    