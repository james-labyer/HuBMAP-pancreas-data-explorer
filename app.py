import pandas as pd
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div(
  children=[
    html.Header(children=[
      html.H1("Spatial Proteome Map of a Single Human Islet Microenvironment")
    ]),
    html.Main(children=[
      dbc.Nav(
        [
          dbc.NavLink("Download Data", href="#download-dataset"),
          dbc.NavLink("Proteome Cross-Section View", href="#cross-section"),
          dbc.NavLink("Proteomics Scatter Plot", href="#scatter-plot")
        ],
        vertical=True
      ),
      html.Div(children=[
      html.Section(
        id="download-dataset",
        children=[
          html.Header(html.H2("Download Data Here")),
          html.P("placeholder text")
        ]
      ),
      html.Section(
        id="cross-section",
        children=[
          html.Header(html.H2("Proteome Cross-Section View")),
          html.P("placeholder text")
        ]
      ),
      html.Section(
        id="scatter-plot",
        children=[
          html.Header(html.H2("Proteomics Scatter Plot")),
          html.P("placeholder text")
        ]
      )
      ])

    ]),
    html.Footer("This site made possible by the Texas Advanced Computing Center.")
  ]
)

if __name__ == "__main__":
  app.run_server(debug=True)