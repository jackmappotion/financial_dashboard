import plotly.graph_objects as go
from plotly.subplots import make_subplots

def draw_macro_graph(df, indicator_1, indicator_2):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df["date"], y=df[indicator_1],
                             mode="lines", name=indicator_1,
                             line=dict(color="blue")),
                  secondary_y=False)

    fig.add_trace(go.Scatter(x=df["date"], y=df[indicator_2],
                             mode="lines", name=indicator_2,
                             line=dict(color="red", dash="dot")),
                  secondary_y=True)

    fig.update_layout(
        title=f"{indicator_1} vs {indicator_2} 변화",
        xaxis_title="Date",
        yaxis=dict(title=indicator_1, color="blue"),
        yaxis2=dict(title=indicator_2, color="red", overlaying="y", side="right"),
        legend=dict(x=0.02, y=1),
        template="plotly_white"
    )
    return fig
