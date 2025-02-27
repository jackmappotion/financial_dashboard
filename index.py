from dash import dcc, html
import dash_bootstrap_components as dbc

# 사이드바 레이아웃
sidebar = dbc.Nav(
    [
        html.Br(),  # 간격 추가
        dbc.NavLink("📊 거시경제 지표", href="/macro", active="exact"),
        dbc.DropdownMenu(
            label="📈 기술적분석 지표",
            children=[
                dbc.DropdownMenuItem("가격 지표", href="/technical/price"),
                dbc.DropdownMenuItem("LOWESS 지표", href="/technical/lowess"),
                dbc.DropdownMenuItem("SPLINE 지표", href="/technical/spline"),
            ],
            nav=True),
        dbc.DropdownMenu(
            label="📓 기본적분석 지표",
            children=[
                dbc.DropdownMenuItem("재무제표 테이블", href="/fundamental/fs_table"),
                dbc.DropdownMenuItem("재무제표 그래프", href="/fundamental/fs_graph"),
                dbc.DropdownMenuItem("시장-내재 평가", href="/fundamental/fs_inidicator"),
            ],
            nav=True)
    ],
    vertical=True,
    pills=True,
    className="p-2"
)

# 메인 레이아웃


def create_layout():
    return dbc.Container([
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col(sidebar, width=2, className="bg-light"),
            dbc.Col(html.Div(id='page-content'), width=10)
        ])
    ], fluid=True)
