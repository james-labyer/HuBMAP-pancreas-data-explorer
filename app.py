import pandas as pd
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

app = Dash(external_stylesheets=[dbc.themes.LUMEN])

df = pd.read_csv('assets/rectangles_output.csv')

X = df.loc[:, 'X Center']
Y = df.loc[:, 'Y Center']
Z = df.loc[:, 'Z Center']
values = df.loc[:, 'CYB5A']

fig1= go.Figure(
  data=go.Volume(
    x=X,
    y=Y,
    z=Z,
    value=values,
    isomin=-3,
    isomax=1,
    opacity=.5,
    surface_count=180,
    slices_z=dict(show=True, locations=[0.4]),
    caps= dict(x_show=True, y_show=True, z_show=True, x_fill=1),
    colorscale='YlGnBu'
  ))
# default: YlGnBu
# Bluered, Blues, Greens, Greys, Jet, Reds, Viridis, YlGnBu, YlOrRd

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
                html.P("Here is a 3D cross-section of the tissue"),
                dcc.Graph(figure=fig1, className="dcc-graph")
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
                html.Div(
                  children=[
                    html.P("Here is the data collected in this study, available as an Excel file or a VTK file."),
                    dbc.Button("Download Excel Spreadsheet", id="btn-download-xlsx", className="download-button"),
                    dcc.Download(id="download-xlsx"),
                    dbc.Button("Download VTK File", id="btn-download-vtk", className="download-button"),
                    dcc.Download(id="download-vtk")
                  ]
                ),
                html.Hr(),
                html.Div(
                  children=[
                    html.P(
                      children=[
                        "If you would like to visualize this data using the `ili spatial data mapping tool, open the ", 
                        html.A("`ili website", href="http://ili.embl.de/"),
                        ", select 'Volume', and drag and drop the following two files into the viewer:"
                      ] 
                    ),
                  ]
                )
              ]
            ),
          ]
        )
      ]),
    html.Footer("This site made possible by the Texas Advanced Computing Center.")
  ]
)

@callback(
    Output("download-xlsx", "data"),
    Input("btn-download-xlsx", "n_clicks"),
    prevent_initial_call=True,
)

def download_xlsx(n_clicks):
    return dcc.send_file(
        "assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.xlsx"
)

@callback(
    Output("download-vtk", "data"),
    Input("btn-download-vtk", "n_clicks"),
    prevent_initial_call=True,
)

def download_vtk(n_clicks):
    return dcc.send_file(
        "assets/HubMAP_TMC_p1_20C_3D_protINT_May8_sorted.vti"
)

if __name__ == "__main__":
  app.run_server(debug=True)