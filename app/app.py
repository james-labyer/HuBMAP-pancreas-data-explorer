from dash import (
    Dash,
    html,
    dcc,
    page_container,
    page_registry,
    callback,
    Output,
    Input,
    State,
)
import dash_bootstrap_components as dbc
import argparse
import logging
import socket


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

    args = parser.parse_args()

    format_str = f"[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s"

    logging.basicConfig(level=args.loglevel, format=format_str)


footer = "\u00a9" + " 2024, Texas Advanced Computing Center"

layout = html.Div(
    children=[
        dcc.Location(id="url"),
        html.Header(
            dbc.Container(
                [
                    dbc.Navbar(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Img(
                                                src="assets/magnifying-glass-chart-solid.svg",
                                                className="text-light header-img",
                                            ),
                                            html.H1(
                                                [
                                                    "HuBMAP Pancreas Data Explorer",
                                                ],
                                                className="bg-primary text-light title",
                                            ),
                                        ],
                                        width=True,
                                        class_name="title-group",
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.NavbarToggler(
                                                id="navbar-toggler",
                                                n_clicks=0,
                                            ),
                                            dbc.Collapse(
                                                dbc.Nav(
                                                    [
                                                        dbc.NavItem(
                                                            dbc.NavLink(
                                                                "All Data",
                                                                href="/",
                                                                class_name="text-light",
                                                            )
                                                        ),
                                                        dbc.NavItem(
                                                            dbc.NavLink(
                                                                "3D Model",
                                                                href="/3d",
                                                                class_name="text-light",
                                                            )
                                                        ),
                                                    ],
                                                    pills=True,
                                                    horizontal="end",
                                                    navbar=True,
                                                ),
                                                id="navbar-collapse",
                                                is_open=False,
                                                navbar=True,
                                            ),
                                        ],
                                        width=2,
                                        md=3,
                                    ),
                                ],
                                justify="between",
                                class_name="w-100",
                                align="center",
                            ),
                        ],
                        class_name="bg-primary text-light w-100",
                        color="primary",
                        dark=True,
                        sticky="top",
                    ),
                    html.Div(id="breadcrumb"),
                ],
                fluid=True,
                class_name="px-0",
            ),
        ),
        html.Main(
            dbc.Container(
                page_container,
                id="content-div",
                class_name="main-div",
            )
        ),
        html.Footer(footer),
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
    if "-optical-clearing-" in pathname:
        # find the current page in the page registry
        this_page = {}
        for page in page_registry.values():
            if page["relative_path"] == pathname:
                this_page = page
                break
        # break out the parts of the path
        parts = pathname.split("/")
        # get first six characters of final path child and make them upper case
        block = parts[1][:6].upper()
        if block[-1] == "-":
            block = block[:5]
        bc = dbc.Breadcrumb(
            items=[
                {"label": "Home", "href": "/", "external_link": False},
                {
                    "label": f"{block} optical clearing",
                    "href": f"/{parts[1]}",
                    "external_link": False,
                },
                {"label": f"{this_page['title']}", "active": True},
            ],
        )
        return bc
    else:
        pass


if __name__ == "__main__":
    handle_args()
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], use_pages=True)
    server = app.server
    app.layout = layout
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
    )
    server = app.server
    app.layout = layout
