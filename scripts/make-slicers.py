import pandas as pd

img_data = pd.read_csv("imgs.csv")

for i in range(img_data.shape[0]):
    fname = img_data.at[i, "fname"]
    volume = img_data.at[i, "volume"]
    description = img_data.at[i, "description"]
    filename = img_data.at[i, "filename"]
    dname = img_data.at[i, "download"]
    folder = f"assets/optical-clearing-czi/"
    dataset = "P1-14A optical clearing"
    output_file = f"./output/{fname}.py"
    channel_colors = [img_data.at[i, "color1"], img_data.at[i, "color2"]]

    line_test = ""

    if img_data.at[i, "format"] == "czi":
        lines0 = (
            f"from dash import html, dcc, callback, Input, Output, get_app, register_page\n"
            f"import dash_bootstrap_components as dbc\n"
            f"from dash_slicer import VolumeSlicer\n"
            f"from bioio import BioImage\n"
            f"import bioio_czi\n"
            f"\n"
            f'slices_img = BioImage("{folder}{filename}", reader=bioio_czi.Reader)\n'
            f"vols = slices_img.data[0]\n"
        )
    elif img_data.at[i, "channels"] > 1 and img_data.at[i, "slices"] > 1:
        lines0 = (
            f"from dash import html, dcc, callback, Input, Output, get_app, register_page\n"
            f"import dash_bootstrap_components as dbc\n"
            f"from dash_slicer import VolumeSlicer\n"
            f"import numpy as np\n"
            f"import imageio.v3 as iio\n"
            f"\n"
            f"im = iio.imread(\n"
            f"'{folder}{filename}'\n"
            f")\n"
        )
        for k in range(img_data.at[i, "channels"]):
            lines0 += f"temp{k} = []\n"

        slices = img_data.at[i, "slices"]
        lines0 += f"for i in range({slices}):\n"
        for k in range(img_data.at[i, "channels"]):
            lines0 += f"    temp{k}.append(im[i][{k}])\n"
        lines0 += f"vols = []\n"
        for k in range(img_data.at[i, "channels"]):
            lines0 += f"vols.append(np.array(temp{k}))\n"

    else:
        lines0 = (
            f"from dash import html, dcc, callback, Input, Output, get_app, register_page\n"
            f"import dash_bootstrap_components as dbc\n"
            f"from dash_slicer import VolumeSlicer\n"
            f"import numpy as np\n"
            f"import imageio.v3 as iio\n"
            f"\n"
            f"im = iio.imread(\n"
            f"'{folder}{filename}'\n"
            f")\n"
            f"vols = []\n"
        )
        for j in range(img_data.at[i, "channels"]):
            lines0 += f"vols.append(np.expand_dims(im[{j}], axis=0))\n"

    lines1 = (
        f"txt2 =register_page(\n"
        f"    __name__,\n"
        f'    path="/P1-14A-optical-clearing/{volume}",\n'
        f'    title="{description}",\n'
        f")\n"
        f"breadcrumb = dbc.Breadcrumb(\n"
        f"    items=[\n"
        f'        {{"label": "Home", "href": "/", "external_link": False}},\n'
        f"       {{\n"
        f'            "label": "{dataset}",\n'
        f'            "href": "/p1-14a-optical-clearing",\n'
        f'            "external_link": True,\n'
        f"        }},\n"
        f'        {{"label": "{description}", "active": True}},\n'
        f"    ],\n"
        f")\n"
    )

    if "green" in channel_colors:
        lines2 = f'colors = ["#{{:02x}}{{:02x}}{{:02x}}".format(0, i, 0) for i in range(0, 256, 1)]\n'
    elif "red" in channel_colors:
        lines2 = f'colors = ["#{{:02x}}{{:02x}}{{:02x}}".format(i, 0, 0) for i in range(0, 256, 1)]\n'
    else:
        lines2 = ""

    lines3 = ""

    for j in range(img_data.at[i, "channels"]):
        lines3 += f"vol{j} = vols[{j}]\n"
        lines3 += f"slicer{j} = VolumeSlicer(get_app(), vol{j})\n"
        lines3 += f'slicer{j}.graph.config["scrollZoom"] = False\n'

    lines4 = (
        f"layout = [\n"
        f"    breadcrumb,\n"
        f"    html.Section(\n"
        f'        id="{volume}",\n'
        f'        className="slicer-card",\n'
        f"        children=[\n"
        f'            html.Header(html.H2("View {description}")),\n'
        f'            html.P("{dname}"),\n'
        f"            html.Div(\n"
        f"                [\n"
    )

    lines5 = ""
    for j in range(img_data.at[i, "channels"]):
        if img_data.at[i, f"loading{j+1}"] == "no":
            lines5 += f"                    html.Div(\n"
            lines5 += f"                        children=[\n"
            lines5 += f"                            slicer{j}.graph,\n"
            lines5 += f"                            slicer{j}.slider,\n"
            lines5 += f"                            *slicer{j}.stores,\n"
            lines5 += f"                        ],\n"
            lines5 += f'                        className="slicer",\n'
            lines5 += f"                    ),\n"
        else:
            lines5 += f"                    dcc.Loading(\n"
            lines5 += f"                        [\n"
            lines5 += f"                            html.Div(\n"
            lines5 += f"                                children=[\n"
            lines5 += f"                                    slicer{j}.graph,\n"
            lines5 += f"                                    slicer{j}.slider,\n"
            lines5 += f"                                    *slicer{j}.stores,\n"
            lines5 += f"                                ],\n"
            lines5 += f'                                className="slicer",\n'
            lines5 += f"                            ),\n"
            lines5 += f"                        ],\n"
            lines5 += f"                        style={{\n"
            lines5 += f'                            "visibility": "visible",\n'
            lines5 += f'                            "backgroundColor": "transparent",\n'
            lines5 += f'                            "opacity": 0.5,\n'
            lines5 += f"                        }},\n"
            lines5 += f'                        type="dot",\n'
            lines5 += f'                        parent_className="loader-wrapper",\n'
            lines5 += f"                    ),"

    lines6 = (
        f"                ]\n"
        f"            ),\n"
        f"            html.Div(\n"
        f"                children=[\n"
        f'                    html.H2("Download file"),\n'
        f"                    html.P(\n"
        f'                        "The easiest way to open this file is to use Fiji with the Bio-Formats plugin installed."\n'
        f"                    ),\n"
        f"                    dbc.Button(\n"
        f'                        "Download .czi",\n'
        f'                        id="btn-download-{volume}",\n'
        f'                        className="download-button",\n'
        f"                    ),\n"
        f'                    dcc.Download(id="download-{volume}"),\n'
        f"                ]\n"
        f"            ),\n"
        f"        ],\n"
        f"    ),\n"
        f"]\n"
    )

    lines7 = ""
    for j in range(img_data.at[i, "channels"]):
        if (
            img_data.at[i, f"color{j+1}"] == "red"
            or img_data.at[i, f"color{j+1}"] == "green"
        ):
            lines7 += f"@callback(\n"
            lines7 += f'    Output(slicer{j}.overlay_data.id, "data"),\n'
            lines7 += f'    Input("{volume}", "children"),\n'
            lines7 += f'    Input(slicer{j}.slider, "value"),\n'
            lines7 += f")\n"
            lines7 += f"def apply_overlay(level, children):\n"
            lines7 += f"    return slicer{j}.create_overlay_data(vol{j}, colors)\n"
    lines8 = (
        f"@callback(\n"
        f'    Output("download-{volume}", "data"),\n'
        f'    Input("btn-download-{volume}", "n_clicks"),\n'
        f"    prevent_initial_call=True,\n"
        f")\n"
        f"def download_czi(n_clicks):\n"
        f"    return dcc.send_file(\n"
        f'        "{folder}{dname}"'
        f"    )\n"
    )

    with open(output_file, "a") as f:
        f.write(lines0)
        f.write(lines1)
        f.write(lines2)
        f.write(lines3)
        f.write(lines4)
        f.write(lines5)
        f.write(lines6)
        f.write(lines7)
        f.write(lines8)
