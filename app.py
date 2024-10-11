import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div(
  children=[
    html.Header(children=[
      html.H1("Spatial Proteome Map of a Single Human Islet Microenvironment")
    ]),
    html.Main(
      id="main-content",
        children=[
        html.Div(
          id="navbar",
          children=[
            dbc.Nav(
              [
                dbc.NavLink("Proteome Cross-Section View", href="#cross-section", external_link=True),
                dbc.NavLink("Proteomics Scatter Plot", href="#scatter-plot", external_link=True),
                dbc.NavLink("Download Data", href="#download-dataset", external_link=True),
              ],
              vertical=True,
            )
          ]
        ),
        html.Div(
          id="content-div",
          children=[
            html.Section(
              id="cross-section",
              children=[
                html.Header(html.H2("Proteome Cross-Section View")),
                html.P("Explanation text"),
                html.Div("Visualization placeholder", className="viz-placeholder")
              ]
            ),
            html.Section(
              id="scatter-plot",
              children=[
                html.Header(html.H2("Proteomics Scatter Plot")),
                html.P("Explanation text"),
                html.Div("Visualization placeholder", className="viz-placeholder")
              ]
            ),
            html.Section(
              id="download-dataset",
              children=[
                html.Header(html.H2("Download Data Here")),
                html.P("Explanation text"),
                html.Button("Download Text", id="btn-download-txt"),
                dcc.Download(id="download-text")
              ]
            ),
          ]
        )
      ]),
    html.Footer("This site made possible by the Texas Advanced Computing Center.")
  ]
)

@callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dict(content="Hello world!", filename="hello.txt")

if __name__ == "__main__":
  app.run_server(debug=True)