from flask import Blueprint, render_template
import json
import plotly
import plotly.graph_objects as go

from models import candle_pairs
import datetime

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return 'Hi'


@routes.route('/graph/<string:pair>')
def graph(pair: str):
    data: list = candle_pairs[pair.upper()].query.all()

    candle_data = [go.Candlestick(
        x=[datetime.datetime.utcfromtimestamp(x.time) for x in data],
        open=[x.open for x in data],
        high=[x.high for x in data],
        low=[x.low for x in data],
        close=[x.close for x in data],
        increasing=dict(line=dict(color='green')),
        decreasing=dict(line=dict(color='red'))
    )]

    volume_data = [go.Bar(
        x=[datetime.datetime.utcfromtimestamp(x.time) for x in data],
        y=[x.volume for x in data])
    ]

    graph_data = json.dumps(candle_data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('graph.html', plot=graph_data)
