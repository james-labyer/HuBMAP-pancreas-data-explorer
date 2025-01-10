import dash_bootstrap_components as dbc
from dash import (
    Dash,
    dcc,
    html,
    page_container,
)
import os
import sys
from flask import Flask
import logging
import socket

os.chdir("..")
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
os.chdir("./config_portal")
from components import header

print(header.get_title())
title = header.get_title() + " Configuration"


# layout function
def serve_layout():
    return html.Div(
        children=[
            dcc.Location(id="config-url"),
            header.make_header("config"),
            html.Main(
                dbc.Container(
                    page_container,
                    id="config-content-div",
                    class_name="main-div",
                )
            ),
            header.footer,
        ]
    )


# Flask setup
server = Flask(__name__)


# Dash setup
app = Dash(
    __name__,
    server=server,
    use_pages=True,
    prevent_initial_callbacks="initial_duplicate",
    suppress_callback_exceptions=True,
    title=title,
    external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP],
)

app.layout = serve_layout

if __name__ == "__main__":
    format_str = f"[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s"
    logging.basicConfig(level="DEBUG", format=format_str)
    app.run(host="0.0.0.0", port="8040", debug=True)
