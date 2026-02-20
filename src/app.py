import dash
from dash import html
import dash_bootstrap_components as dbc
import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv
import dash_mantine_components as dmc

from logs import get_logger

load_dotenv(find_dotenv())

logger = get_logger(__name__)

flask_server = Flask(__name__)

dash_app = dash.Dash( 
    __name__,
    use_pages=True,
    server=flask_server,
    external_stylesheets=[
        # dbc.themes.BOOTSTRAP,
        os.path.join("src", "assets", "styles.css"),
        os.path.join("src", "assets", "bootstrap.min.css"),
        "https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap",
    ],
    title="ChatRMG",
    suppress_callback_exceptions=True,
)

dash_app.layout = dmc.MantineProvider(html.Div(
    children=[dash.page_container],
    className="container-fluid",
    style={
        "width": "100%",
        "height": "100%",
        "overflow": "hidden",
    },
))

if __name__ == "__main__":
    dash_app.run(debug=True, port=8051, host='0.0.0.0')