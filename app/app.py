from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], use_pages=True)

server = app.server

app.layout = html.Div(
    children=[
        html.Header(
            dbc.Container(
                dbc.Navbar(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H1(
                                        "HuBMAP Pancreas Data Explorer",
                                        className="bg-primary text-light title",
                                    ),
                                    width=True,
                                ),
                                dbc.Col(
                                    dbc.Nav(
                                        [
                                            dbc.NavItem(
                                                dbc.NavLink(
                                                    "All Datasets",
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
                                    width=3,
                                ),
                            ],
                            justify="between",
                            class_name="w-100",
                            align="center",
                        ),
                    ],
                    class_name="bg-primary text-light w-100",
                    color="primary",
                    sticky="top",
                ),
                fluid=True,
                class_name="px-0",
            ),
        ),
        html.Div(id="my-output"),
        page_container,
        html.Footer("Copyright 2024, Texas Advanced Computing Center"),
    ]
)


if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port="8050",
        debug=True,
        dev_tools_props_check=False,
    )
