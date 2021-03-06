from io import BytesIO

from flask import Blueprint, render_template, url_for, make_response
import requests
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from ._generate_graph import create_plot

argo_app = Blueprint('argo_app', __name__, template_folder='templates')


@argo_app.route("/")
def index():
    """
    Route to represent the Map.

        This is the single page of the application.

    :return: request
    """
    return render_template('map.html')


@argo_app.route("/info/<identifier>")
def info_text(identifier):
    """
    Route to get the ArgoFloat info-block.

    :param identifier: str - Identifier of the ArgoFloat
    :return: request
    """
    url = url_for('argo_api.get_argo_float', identifier=identifier, _external=True)
    data = requests.get(url).json()

    return render_template('_info_text.html', data=data)


@argo_app.route("/chart/<identifier>")
def deliver_chart(identifier=None):
    """
    Route to get the chart-picture of the measurement data.

    :param identifier: str - Identifier of the ArgoFloat
    :return: request  - contains the canvas object of the graph.
    """
    if identifier is None:
        return

    # Send get-response to the api-url.
    # This will return json with the data of the specified argofloat.
    url = url_for('argo_api.get_argo_float', identifier=identifier, _external=True)
    data = requests.get(url).json()

    # The fig is the actual Plot.
    fig = create_plot(data)
    # To deliver the Plot, this have to drawed into a canvas/png picture.
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    # Directly add the png to the response.
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response
