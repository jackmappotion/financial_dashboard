from dash import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def df2data_table(df):
    data_table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in df.columns],
        style_cell={'textAlign': 'left'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        column_selectable="single",
    )
    return data_table


def df2plotly_fig(df):
    title = df.iloc[0]['name'] + '-' + df.iloc[0]['sector']
    cols = df.drop(columns=['name', 'sector']).columns
    fig = go.Figure(
        data=[go.Table(
            header=dict(values=list(cols),
                        fill_color='paleturquoise',
                        align='left',
                        ),
            cells=dict(values=[df[col] for col in cols],
                       fill_color='lavender',
                       align='left',
                       ))
              ])
    fig.update_layout(
        title=dict(text=title, font=dict(size=30), automargin=False)
    )
    return fig


def plot_stock_sector_fig(stock_sector_df, stock_name, sector_name):
    fig = make_subplots(
        rows=1, cols=3,  # 1 Row, 3 Columns
        subplot_titles=stock_sector_df['index']  # 각 subplot의 제목 설정
    )

    # 각 subplot에 데이터 추가
    for i, metric in enumerate(stock_sector_df['index']):
        fig.add_trace(go.Bar(
            x=['Stock', 'Sector'],
            y=[stock_sector_df['stock'][i], stock_sector_df['sector'][i]],
            name=metric,
            marker_color=['blue', 'red']
        ), row=1, col=i + 1)

    # 전체 레이아웃 설정
    fig.update_layout(
        title=f"{stock_name} vs {sector_name}",
        showlegend=False  # 개별 subplot에 범례가 필요 없으므로 숨김
    )
    return fig


def draw_fundamental_graph(df, title, indicator_1, indicator_2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df.index, y=df[indicator_1],
                             mode="lines", name=indicator_1,
                             line=dict(color="blue")),
                  secondary_y=False)

    fig.add_trace(go.Scatter(x=df.index, y=df[indicator_2],
                             mode="lines", name=indicator_2,
                             line=dict(color="red", dash="dot")),
                  secondary_y=True)

    fig.update_layout(
        title=f"{title}",
        xaxis_title="Date",
        yaxis=dict(title=indicator_1, color="blue"),
        yaxis2=dict(title=indicator_2, color="red", overlaying="y", side="right"),
        legend=dict(x=0.02, y=1),
        template="plotly_white"
    )
    return fig
