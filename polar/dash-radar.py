import math
from datetime import datetime

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

dash_app = Dash(__name__)

BR = "<br>"
ONLY_SOLAR = 'onlysolar'


theta = ["{}:00".format(n) for n in range(24)]
no_fill_theta = list(theta)
no_fill_theta.append(theta[0])
width = [1] * 24
df = pd.read_csv('hourly-predicted.csv')
df[ONLY_SOLAR] = df['solarUsage'] + df['curtailedEnergy'] + df['storageDischarge']
df['discharge'] = df['coalGen'] + df['gasGen'] + df['storageGasCharge'] + df['windGen'] + df['solarUsage'] \
                  + df['storageSolarCharge'] + df['curtailedEnergy'] + df['storageDischarge']

TICK_STEP = 20000
max_tick = math.ceil(df['discharge'].max()/TICK_STEP)*TICK_STEP
tickvals = [i*TICK_STEP for i in range(1, int(max_tick/TICK_STEP))]

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


def date_str(day_of_year):
    return datetime.strptime(df['date'][day_of_year * 24], "%m/%d/%Y").strftime("%-d %B, %Y")


def annotation(day_of_year):
    return "<span style='font-weight:bolder;color:black;font-size: 20px'>" + date_str(day_of_year) + "</span>" \
           + BR + BR \
           + "<span style='color:red';font-size: 16px>Total Demand: {:.2f} KWh"\
                    .format(df_by_date['demand'][day_of_year]/1000) + '</span>' + BR \
           + "<span style='color:orange;font-size: 16px'>Solar Power: {:.2f} KWh" \
                    .format(df_by_date[ONLY_SOLAR][day_of_year]/1000) + '</span>' + BR


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
    f.add_annotation(xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, text=annotation(day_of_year),
                     font=dict(family="Arial", size=16, color="black"))
    return f


def plot(day_of_year):
    f = barplot(day_of_year)
    f.update_layout(
        height=800,
        polar=dict(
            hole=0.4,
            radialaxis=dict(visible=True,
                            range=[0, max_tick],
                            tickvals=tickvals,
                            tickfont=dict(color="black"),
                            tickangle=30),
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
        children=[
            html.Div(children=[
                dcc.Graph(figure=heatmap('demand', "reds"), config={'displayModeBar': False}),
                dcc.Graph(figure=heatmap(ONLY_SOLAR, [[0, 'white'], [0.8, 'gold'], [1, 'orange']]),
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
                               id="date-slider",
                               ),
                ]),
        ],
    ),
    html.Div(className="row", children=[
        html.Div(
            [dcc.Slider(
                min=2020,
                max=2050,
                step=1,
                value=2050,
                marks={y: str(y) for y in range(2020, 2051, 10)},
                id="year-slider",
                vertical=True,
                verticalHeight=600)],
            style={'width': '7%', 'display': 'inline-block'}
        ),
        html.Div(
            dcc.Graph(id="daily-radar-plot", config={'displayModeBar': False}),
            style={'width': '90%', 'display': 'inline-block', 'vertical-align': 'top'}
        )
    ])
])


@dash_app.callback(
    Output("daily-radar-plot", "figure"),
    [Input("date-slider", "value"), Input("year-slider", "value")])
def update_radar(day_of_year, year):
    # year is ignored for now
    fig = plot(day_of_year)
    return fig


dash_app.run_server(debug=True, port=9995)
