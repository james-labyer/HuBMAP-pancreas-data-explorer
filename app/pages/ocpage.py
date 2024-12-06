import logging

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html, no_update, register_page
from PIL import Image

app_logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger("gunicorn.error")
app_logger.handlers = gunicorn_logger.handlers
app_logger.setLevel(gunicorn_logger.level)


def title(oc=None, pancreas=None, block=None):
    return f"{oc} optical clearing"


register_page(
    __name__,
    path_template="/optical-clearing/<pancreas>/<block>/<oc>",
    path="/optical-clearing/P1/P1-19A/P1-19A-1",
    title=title,
)

oc_imgs = pd.read_csv("assets/optical-clearing-czi/oc-files.csv")


def make_tab_content(slider=False, points=0, channels=1):
    card_content = []
    body_content = [
        html.Div(
            id="oc-slider-output",
            className="custom-slicer-div",
        ),
    ]

    if channels <= 1:
        # tabs element must exist so the callback will work; style hides it
        card_content.append(
            dbc.Tabs([], id="tabs", active_tab="channel-1", style={"display": "none"})
        )
    else:
        tabs = []
        for i in range(channels):
            tabs.append(dbc.Tab(label=f"Channel {i + 1}", tab_id=f"channel-{i + 1}"))
        card_content.append(
            dbc.CardHeader(
                dbc.Tabs(
                    tabs,
                    id="tabs",
                    active_tab="channel-1",
                )
            ),
        )

    if slider:
        body_content.append(
            dcc.Slider(
                1,
                points,
                1,
                value=1,
                id="oc-slider",
            ),
        )

    card_content.append(dbc.CardBody(body_content))
    return dbc.Card(card_content, class_name="slicer-card")


def make_download_section(filename):
    return html.Div(
        children=[
            html.H2("Download original file", className="download-header"),
            html.P(filename),
            dbc.Button(
                "Download",
                id="btn-download-oc",
                className="download-button",
            ),
            dcc.Download(id="download-oc"),
        ]
    )


def layout(oc=None, **kwargs):
    # handle bad oc values
    img = oc_imgs.loc[(oc_imgs["oc"] == oc)]
    if img.empty:
        return html.Div(html.P("Invalid optical clearing requested"))

    # flatten dict since there is only one row
    img_dict = {
        "block": img.at[img.index[0], "block"],
        "oc": img.at[img.index[0], "oc"],
        "file": img.at[img.index[0], "file"],
        "basefile": img.at[img.index[0], "basefile"],
        "slices": img.at[img.index[0], "slices"],
        "channels": img.at[img.index[0], "channels"],
        "height": img.at[img.index[0], "height"],
        "width": img.at[img.index[0], "width"],
    }
    oc = img_dict["oc"].split("-")
    return html.Div(
        [
            html.H2(f"{img_dict['block']} Optical Clearing {oc[-1]}"),
            make_tab_content(
                (img_dict["slices"] > 1),
                img_dict["slices"],
                img_dict["channels"],
            ),
            dcc.Store(id="oc-slider-store"),
            dcc.Store(id="oc-file-store", data=img_dict),
            make_download_section(img_dict["file"]),
        ]
    )


@callback(Output("oc-slider-store", "data"), Input("oc-slider", "value"))
def save_slider_pos(value):
    return value


@callback(
    Output("oc-slider-output", "children"),
    Input("tabs", "active_tab"),
    Input("oc-slider-store", "data"),
    State("oc-file-store", "data"),
)
def update_pic(tab, slider, data):
    # callbacks must be included in the page even though not all layouts need them
    # no_update supresses the callback if not needed for this path
    if not tab and not slider:
        return no_update
    elif not slider:
        val_str = "0000"
    else:
        val = slider - 1
        val_str = f"{val:04}"

    if not tab:
        c = 0
    else:
        c = int(tab[-1]) - 1

    pic = Image.open(
        f"assets/optical-clearing-czi/{data['block']}/{data['basefile']}/{data['basefile']}_C{c}{val_str}.png"
    )
    # add max-height and max-width to style based on image's dimensions
    return html.Img(
        src=pic,
        className="custom-slicer-img solo-slicer-img",
        style={"max-height": data["height"], "max-width": data["width"]},
    )


@callback(
    Output("download-oc", "data"),
    Input("btn-download-oc", "n_clicks"),
    State("oc-file-store", "data"),
    prevent_initial_call=True,
)
def download_file(n_clicks, data):
    app_logger.debug(f"Sending {data['file']}")
    return dcc.send_file(
        f"assets/optical-clearing-czi/{data['block']}/{data['basefile']}/{data['file']}"
    )
