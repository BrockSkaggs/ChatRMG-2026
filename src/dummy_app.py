import dash
from dash import html


dash_app = dash.Dash(__name__)


dash_app.layout = html.Div([
    "Hello World"
])


if __name__ == "__main__":
    dash_app.run(debug=True, host='0.0.0.0')