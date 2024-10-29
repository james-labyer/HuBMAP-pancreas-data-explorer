from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], use_pages=True)

server = app.server

app.layout = html.Div(
    children=[
        html.Header(
            children=[
                html.Div(
                    id="navbar",
                    children=[
                        dbc.Navbar(
                            [
                                dbc.Container(
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
                                                dbc.Button(
                                                    "View All Datasets",
                                                    href="/",
                                                    external_link=False,
                                                    color="secondary",
                                                    className="all-data",
                                                ),
                                                width=3,
                                                xl=2,
                                            ),
                                        ],
                                        align="center",
                                        justify="between",
                                        class_name="w-100",
                                    ),
                                    fluid=True,
                                )
                            ],
                            color="primary",
                            sticky="top",
                        ),
                    ],
                ),
            ]
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
