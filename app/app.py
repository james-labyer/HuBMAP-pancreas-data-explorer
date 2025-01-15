import argparse
import logging
import socket

import dash_bootstrap_components as dbc
import pandas as pd
from dash import (
    Dash,
    Input,
    Output,
    State,
    callback,
    dcc,
    html,
    page_container,
)
import os
import sys
from flask import Flask, request

os.chdir("..")
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
os.chdir("./app")
from components import header


def handle_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--loglevel",
        type=str,
        required=False,
        default="WARNING",
        help="set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL",
    )

    return parser.parse_args()


# Flask setup
server = Flask(__name__)


@server.route("/title", methods=["POST"])
def update_title():
    labels = pd.read_csv("../config/labels.csv")
    # need to escape?
    labels.at[0, "title"] = request.get_json()["title"]
    labels.to_csv("../config/labels.csv")
    # This title update only works temporarily
    # app.title = request.get_json()["title"]
    return "", 204


@server.route("/block-data", methods=["POST"])
def update_block_data():
    file = request.files["file"]
    file.save("../config/blocks.csv")
    return "", 204


@server.route("/si-files", methods=["POST"])
def update_si_files():
    file = request.files["file"]
    file.save("../config/image-sets.csv")
    return "", 204


def serve_layout():
    return html.Div(
        children=[
            dcc.Location(id="url"),
            header.make_header("app"),
            html.Main(
                dbc.Container(
                    page_container,
                    id="content-div",
                    class_name="main-div",
                )
            ),
            header.footer,
        ]
    )


@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(Output("breadcrumb", "children"), [Input("url", "pathname")])
def render_breadcrumb(pathname):
    if pathname and "/scientific-images/" in pathname and len(pathname) > 28:
        # break out the parts of the path
        parts = pathname.split("/")
        # get first six characters of final path child and make them upper case
        block = parts[-1][:6].upper()
        if block[-1] == "-":
            block = block[:5]
        oc = parts[-1].split("-")
        bc = dbc.Breadcrumb(
            items=[
                {"label": "Home", "href": "/", "external_link": False},
                {
                    "label": f"{block} scientific image sets",
                    "href": f"/scientific-images-list/{parts[-2]}",
                    "external_link": False,
                },
                {"label": f"{block} scientific image set {oc[-1]}", "active": True},
            ],
        )
        return bc
    else:
        pass


if __name__ == "__main__":
    args = handle_args()
    format_str = f"[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s"
    logging.basicConfig(level=args.loglevel, format=format_str)
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.LUMEN],
        use_pages=True,
        server=server,
        title=header.get_title(),
    )
    # server = app.server
    app.layout = serve_layout
    app.run_server(
        host="0.0.0.0",
        port="8050",
        debug=True,
        dev_tools_props_check=False,
    )
else:
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.LUMEN],
        use_pages=True,
        server=server,
        title=header.get_title(),
    )
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.debug("Test")
    # server = app.server
    app.layout = serve_layout
