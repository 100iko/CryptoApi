from datetime import datetime, timedelta

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from models import unique_pairs


def init_dash(server):
    dash_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/charts/',
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            '../static/css/dash_style.css',
        ]
    )
    dash_app.title = 'Charts'

    dash_app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        className="m-2",
                        children=[dbc.Select(
                            id='pair',
                            value='BTCUSD',
                            options=[{"label": str(x).upper(), "value": str(x).upper()} for x in unique_pairs],
                        )]),

                    html.Div(
                        className="m-2",
                        children=[dbc.Select(
                            id='interval',
                            value=30,
                            options=[
                                {"label": '1m', "value": 1},
                                {"label": '3m', "value": 3},
                                {"label": '5m', "value": 5},
                                {"label": '15m', "value": 15},
                                {"label": '30m', "value": 30},
                                {"label": '1h', "value": 60},
                                {"label": '2h', "value": 60 * 2},
                                {"label": '3h', "value": 60 * 3},
                                {"label": '4h', "value": 60 * 4},
                                {"label": '6h', "value": 60 * 6},
                                {"label": '12h', "value": 60 * 12},
                                {"label": '1d', "value": 60 * 24},
                            ]
                        )]
                    )], style={"display": "flex", "flexWrap": "wrap"}),

            dcc.Graph(id='chart')
        ], style={"height": "100vh"})

    init_dash_callbacks(dash_app)


def init_dash_callbacks(app):
    @app.callback(
        Output('chart', 'figure'),
        [
            Input('pair', 'value'),
            Input('interval', 'value')
        ]
    )
    def update_graph(pair, interval):
        if pair is None: return
        if interval is None: return

        # candle_type = unique_pairs[pair.upper()]
        # data = candle_type.query.order_by(candle_type.time.desc()).limit(24 * 60).all()
        data = generate_intervals(pair, int(interval))

        time_periods = [datetime.fromtimestamp(x.time) for x in data]

        candle_data = go.Candlestick(
            x=time_periods,
            open=[x.open for x in data],
            high=[x.high for x in data],
            low=[x.low for x in data],
            close=[x.close for x in data],
            increasing=dict(fillcolor='rgb(65, 185, 137)', line=dict(color='rgb(65, 185, 137)')),
            decreasing=dict(fillcolor='rgb(244, 76, 95)', line=dict(color='rgb(244, 76, 95)')),
            name='Price',
            showlegend=False,
        )

        volumes = [x.volume for x in data]
        volume_data = go.Bar(
            x=time_periods,
            y=volumes,
            name='Volume',
        )

        vwap_data = go.Scatter(
            x=time_periods,
            y=list(map(lambda x: x.vwap if x.vwap > 0 else (x.open + x.close) / 2, data)),
            name='Vwap',
            fillcolor='orange',
            mode='markers',
            marker=dict(color='orange', size=3),
            showlegend=False,
        )

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(volume_data, secondary_y=False)
        fig.add_trace(candle_data, secondary_y=True)
        fig.add_trace(vwap_data, secondary_y=True)

        update_layout(fig,
                      time_periods[min(120, len(time_periods) - 1)],
                      time_periods[0] + timedelta(minutes=int(interval) * 5),
                      max(volumes) * 3)

        return fig

    def update_layout(fig, xmin, xmax, ymax):
        fig.layout.update(dict(
            margin=dict(l=8, r=8, t=24, b=12),
            dragmode='pan',
            hovermode='x unified',
            plot_bgcolor='rgb(18, 23, 33)',
            paper_bgcolor='rgb(18, 23, 33)',
            showlegend=False,
            xaxis=dict(
                gridcolor='rgb(36, 41, 55)',
                showgrid=True,
                showspikes=True,
                spikecolor='rgb(152, 152, 152)',
                spikemode='across',
                spikesnap='hovered data',
                spikethickness=1,
                rangeslider=dict(visible=False),
                range=[xmin, xmax]
            ),
            yaxis=dict(
                showspikes=True,
                spikecolor='rgb(152, 152, 152)',
                spikemode='across',
                spikesnap='cursor',
                spikethickness=1,
                fixedrange=True,
                showgrid=False,
                range=[0, ymax],
            ),
            yaxis2=dict(
                gridcolor='rgb(36, 41, 55)',
                showgrid=True
            ),
        ))


def generate_intervals(pair_type, interval: int):
    candle_type = unique_pairs[pair_type.upper()]
    candles = candle_type.query.order_by(candle_type.time.desc()).limit(60 * 24 * 2 * interval).all()[::-1]

    if interval == 1:
        return candles[::-1]

    while (candles[0].time / 60) % interval != 0:
        candles.pop(0)

    while len(candles) % interval != 0:
        candles.pop(-1)

    new_data = []
    for i in range(0, len(candles), interval):
        range_list = candles[i:i + interval]

        new_time = range_list[0].time
        new_open = range_list[0].open
        new_high = max([x.high for x in range_list])
        new_low = min([x.low for x in range_list])
        new_close = range_list[-1].close
        new_volume = sum([x.volume for x in range_list])
        new_vwap = sum(x.vwap * x.volume for x in range_list) / new_volume if new_volume > 0 else 0
        new_count = sum([x.count for x in range_list])

        new_candle = candle_type(new_time, new_open, new_high, new_low, new_close, new_vwap, new_volume, new_count)
        new_data.append(new_candle)

    return new_data[::-1]
