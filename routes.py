from flask import Blueprint, render_template
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from models import candle_pairs
from datetime import datetime, timedelta

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return 'Hi'


@routes.route('/graph/<string:pair>')
def graph(pair: str):
    candle_type = candle_pairs[pair.upper()]
    data: list = candle_type.query.order_by(candle_type.time.desc()).limit(100).all()

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

    volume_data = go.Bar(
        x=time_periods,
        y=[x.volume for x in data],
        name='Volume',
        meta=dict(colorbar="#FFFFFF")
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(volume_data, secondary_y=False)
    fig.add_trace(candle_data, secondary_y=True)

    fig.layout.update(dict(
        title=pair.upper(),
        title_x=0.5,
        dragmode='pan',
        hovermode='x unified',
        plot_bgcolor='rgb(18, 23, 33)',
        showlegend=False,
        xaxis=dict(
            gridcolor='rgb(36, 41, 55)',
            showgrid=True,
            range=[datetime.now() - timedelta(hours=4), datetime.now()],
            showspikes=True,
            spikecolor='rgb(152, 152, 152)',
            spikemode='across',
            spikesnap='hovered data',
            spikethickness=1,
            rangeslider=dict(visible=False),
        ),
        yaxis=dict(
            showspikes=True,
            spikecolor='rgb(152, 152, 152)',
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1,
            showgrid=False,
            range=[0, 300],
        ),
        yaxis2=dict(
            gridcolor='rgb(36, 41, 55)',
            showgrid=True
        ),
    ))

    fig.write_html("templates/fig_graph.html")

    return render_template('fig_graph.html')
