import math
from datetime import datetime

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

dash_app = Dash(__name__)


theta = list(["{}:00".format(n) for n in range(24)])
no_fill_theta = list(theta)
no_fill_theta.append(theta[0])
df = pd.read_csv('hourly-predicted.csv')
df['coal'] = df['coalGen']
df['gas'] = df['coal'] + df['gasGen']
df['allgas'] = df['gas'] + df['storageGasCharge']
df['wind'] = df['allgas'] + df['windGen']
df['solar'] = df['wind'] + df['solarUsage']
df['allsolar'] = df['solar'] + df['storageSolarCharge']
df['curtailed'] = df['allsolar'] + df['curtailedEnergy']
df['discharge'] = df['curtailed'] + df['storageDischarge']
max_tick = math.ceil(df['discharge'].max()/20000)*20000
tickvals = [i*20000 for i in range(int(max_tick/20000))]

print("Running")


# denamd and netDemand as lines - maybe use base

def polar_scatter(day, name, color, fill=True):
    r = [0] * 24 if day < 0 else df[name][(day * 24):(day+1)*24]
    if not fill:  # if fill is false then add another point to close the loop
        r = list(r)
        r.append(r[0])
    return go.Scatterpolar(
        name=name,
        r=r,
        theta=theta if fill else no_fill_theta,
        fillcolor=color,
        fill='toself' if fill else "none",
        marker=dict(color=color),
        line=dict(color=color, shape="spline", smoothing=0.2),
    )


def radar(day_of_year):
    f = go.Figure()
    f.add_trace(polar_scatter(day_of_year, "discharge", "lightblue"))
    f.add_trace(polar_scatter(day_of_year, "curtailed", "yellow"))
    f.add_trace(polar_scatter(day_of_year, "allsolar", "gold"))
    f.add_trace(polar_scatter(day_of_year, "solar", "orange"))
    f.add_trace(polar_scatter(day_of_year, "wind", "lightgreen"))
    f.add_trace(polar_scatter(day_of_year, "allgas", "silver"))
    f.add_trace(polar_scatter(day_of_year, "gas", "lightgray"))
    f.add_trace(polar_scatter(day_of_year, "coal", "black"))
    f.add_trace(polar_scatter(-1, "", "white"))
    f.add_trace(polar_scatter(day_of_year, "demand", "red", False))

    date = df['date'][day_of_year * 24]
    f.update_layout(
        title=go.layout.Title(
            x=0.5,
            xanchor='center',
            text=datetime.strptime(date, "%m/%d/%Y").strftime("%d %B, %Y")),
        height=800,
        polar=dict(
            radialaxis=dict(visible=True, range=[-50000, max_tick], tickvals=tickvals, tickfont=dict(color="white")),
            angularaxis=dict(
                tickfont_size=12,
                rotation=270,
                direction="clockwise"
            )
        ),
        showlegend=False,
    )
    return f


dash_app.layout = html.Div([
    html.H1('Daily generation and consumption', style={'textAlign': 'center'}),
    dcc.Slider(0, 364, step=1, marks=None, value=150, id="slider"),
    dcc.Graph(id="daily-radar-plot"),
])


@dash_app.callback(
    Output("daily-radar-plot", "figure"),
    [Input("slider", "value")])
def update_radar(slider):
    fig = radar(slider)
    return fig


dash_app.run_server(debug=True, port=9995)
