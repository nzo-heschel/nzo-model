import math
from datetime import datetime

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

dash_app = Dash(__name__)

theta = ["{}:00".format(n) for n in range(24)]
no_fill_theta = list(theta)
no_fill_theta.append(theta[0])
width = [1] * 24
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

df['onlysolar'] = df['solarUsage'] + df['curtailedEnergy'] + df['storageDischarge']
df_by_date = df.groupby(['date']).sum()
print("Running")


def polar_bar(day, name, color):
    r = df[name][(day * 24):(day+1)*24]
    return go.Barpolar(
        name=name,
        r=r,
        theta=theta,
        width=width,
        marker_color=color,
        hovertemplate='<i>%{theta} : %{r:,.0f} KW</i>'
    )


def polar_scatter(day, name, color, fill=True, dash=False):
    r = df[name][(day * 24):(day+1)*24]
    if not fill:  # if fill is false then add another point to close the loop
        r = list(r)
        r.append(r[0])
    return go.Scatterpolar(
        name=name,
        r=r,
        theta=theta if fill else no_fill_theta,
        fillcolor=color,
        fill="toself" if fill else "none",
        marker=dict(color=color),
        line=dict(color=color, shape="spline", smoothing=0, dash=("dash" if dash else "solid")),
        hoveron="points",
        hovertemplate='<i>%{theta} : %{r:,.0f} KW</i>'
    )


def barplot(day_of_year):
    f = go.Figure()
    f.add_trace(polar_bar(day_of_year, "coalGen", "black"))
    f.add_trace(polar_bar(day_of_year, "gasGen", "lightgray"))
    f.add_trace(polar_bar(day_of_year, "storageGasCharge", "silver"))
    f.add_trace(polar_bar(day_of_year, "windGen", "lightgreen"))
    f.add_trace(polar_bar(day_of_year, "solarUsage", "orange"))
    f.add_trace(polar_bar(day_of_year, "storageSolarCharge", "gold"))
    f.add_trace(polar_bar(day_of_year, "curtailedEnergy", "yellow"))
    f.add_trace(polar_bar(day_of_year, "storageDischarge", "lightblue"))
    f.add_trace(polar_scatter(day_of_year, "demand", "red", False))
    f.add_trace(polar_scatter(day_of_year, "netDemand", "purple", False, True))
    return f


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
    f.add_trace(polar_scatter(day_of_year, "demand", "red", False))
    f.add_trace(polar_scatter(day_of_year, "netDemand", "purple", False, True))
    return f


def plot(day_of_year, bar):
    f = barplot(day_of_year) if bar else radar(day_of_year)
    date = df['date'][day_of_year * 24]
    f.update_layout(
        title=go.layout.Title(
            x=0.5,
            xanchor='center',
            text=datetime.strptime(date, "%m/%d/%Y").strftime("%d %B, %Y")),
        height=800,
        polar=dict(
            hole=0.4,
            radialaxis=dict(visible=True,
                            range=[0, max_tick],
                            tickvals=tickvals,
                            tickfont=dict(color="white"),
                            tickangle=90),
            angularaxis=dict(
                tickfont_size=12,
                rotation=270,
                direction="clockwise"
            )
        ),
        showlegend=True,
    )
    return f


def marks(year):
    result = {}
    for month in range(1, 13):
        timestamp = pd.Timestamp(year, month, 1)
        day = timestamp.dayofyear
        result[day] = "|"
        result[day + 15] = timestamp.month_name()
    result[pd.Timestamp(year, 12, 31).dayofyear - 1] = "|"
    return result


def yearly():
    f = go.Figure(
        data=[go.Scatter(y=df_by_date['demand'], marker_color="red"),
              go.Scatter(y=df_by_date['onlysolar'], marker_color="gold")],
    )
    f.update_layout(
        showlegend=False,
        height=40,
        xaxis={'fixedrange': True, 'visible': False},
        yaxis={'fixedrange': True, 'visible': False},
        margin=dict(l=25, r=25, t=0, b=0),
        plot_bgcolor="white"
    )
    return f


def heatmap(name, pallette):
    f = go.Figure(
        go.Heatmap(z=[df_by_date[name]], showscale=False, colorscale=pallette)
    )
    f.update_layout(
        showlegend=False,
        height=30,
        xaxis={'fixedrange': True, 'visible': False},
        yaxis={'fixedrange': True, 'visible': False},
        margin=dict(l=28, r=25, t=0, b=0),
    )
    return f


dash_app.layout = html.Div([
    html.H1('Daily generation and consumption', style={'textAlign': 'center'}),
    html.Div(
        style={'position': 'relative'},
        # style={'backgroundColor':'white'},
        children=[
            html.Div(children=[
                dcc.Graph(figure=heatmap('wind', [[0, 'white'], [1, 'red']]), config={'displayModeBar': False}),
                dcc.Graph(figure=heatmap('onlysolar', [[0, 'white'], [0.8, 'gold'], [1, 'orange']]),
                          config={'displayModeBar': False}),
            ]),
            html.Div(
                style={'position': 'absolute', 'top': 23, 'width': '100%'},
                children=[
                    dcc.Slider(min=0,
                               max=pd.Timestamp(2050, 12, 31).dayofyear - 1,
                               step=1,
                               value=pd.Timestamp(2050, 6, 1).dayofyear - 1,
                               marks=marks(2050),
                               id="slider",
                               ),
                ]),
        ],
    ),
    dcc.Checklist(["Bar or Scatter"], id="bar-or-scatter"),
    dcc.Graph(id="daily-radar-plot", config={'displayModeBar': False}),
])


@dash_app.callback(
    Output("daily-radar-plot", "figure"),
    [Input("slider", "value"), Input("bar-or-scatter", "value")])
def update_radar(slider, bar):
    fig = plot(slider, bar and "Bar or Scatter" in bar)
    return fig


dash_app.run_server(debug=True, port=9995)
