import pandas as pd
from dash import html, dash_table, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/', title="HuBMAP Pancreas Data Explorer")

blocks = pd.read_csv("assets/block-data.csv")

block_table = dash_table.DataTable(
    data=blocks.to_dict('records'),
    columns=[{'id': c, 'name': c, 'presentation': 'markdown'} if c == 'Optical clearing' or c == 'GeoMX' or c =='Proteomics' else {'id': c, 'name': c} for c in blocks.columns],
    style_as_list_view=True,
    style_cell={
        'textAlign': 'left',
        'font-family': 'Source Sans Pro',
        'padding': '8px 10px 8px 10px'
        },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#fafafa',
        }
    ],
    style_header={
        'backgroundColor': '#f0f0f0',
        'color': 'black',
        'fontWeight': 'bold'
    },
    id="block-table"
)

layout = html.Div(
    children=[
        html.Main(
            id="main-content",
            children=[
                dbc.Container(
                    id="content-div",
                    children=[
                        html.Section(
                            [
                                html.Header(html.H2("Pancreas 1 Datasets")),
                                block_table
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ]
)