import pandas as pd

img_data = pd.read_csv("imgs.csv")

for i in range(12):
    volume = img_data.at[i, "volume"]
    description = img_data.at[i, "description"]
    filename = img_data.at[i, "filename"]
    filepath = f"assets/optical-clearing-czi/{filename}"
    dataset = "P1-14A optical clearing"
    output_file = f"./output/{volume}.py"
    channel_colors = [img_data.at[i, "color1"], img_data.at[i, "color2"]]

    lines1 = (
        f"from dash import html, callback, Input, Output, get_app, register_page\n"
        f"import dash_bootstrap_components as dbc\n"
        f"from dash_slicer import VolumeSlicer\n"
        f"from bioio import BioImage\n"
        f"import bioio_czi\n"
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
        f'            "href": "/layout2",\n'
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

    lines3 = (
        f'slices_img = BioImage("{filepath}", reader=bioio_czi.Reader)\n'
        f"vol = slices_img.data[0][0]\n"
        f"slicer1 = VolumeSlicer(get_app(), vol)\n"
        f'slicer1.graph.config["scrollZoom"] = False\n'
    )

    if not pd.isna(img_data.at[i, "color2"]):
        lines4 = (
            f"vol2 = slices_img.data[0][1]\n"
            f"slicer2 = VolumeSlicer(get_app(), vol2)\n"
            f'slicer2.graph.config["scrollZoom"] = False\n'
        )
        lines5 = (
            f"layout = [\n"
            f"    breadcrumb,\n"
            f"    html.Section(\n"
            f'        id="{volume}",\n'
            f'        className="slicer-card",\n'
            f"        children=[\n"
            f'            html.Header(html.H2("View {description}")),\n'
            f'            html.Header(html.P("{filename}")),\n'
            f"            html.Div(\n"
            f"                [\n"
            f"                    html.Div(\n"
            f"                        children=[\n"
            f"                            slicer1.graph,\n"
            f"                            slicer1.slider,\n"
            f"                            *slicer1.stores,\n"
            f"                        ],\n"
            f"                    ),\n"
            f"                    html.Div(\n"
            f"                        children=[\n"
            f"                            slicer2.graph,\n"
            f"                            slicer2.slider,\n"
            f"                            *slicer2.stores,\n"
            f"                        ],\n"
            f"                    ),\n"
            f"                ]\n"
            f"            ),\n"
            f"        ],\n"
            f"    ),\n"
            f"]\n"
        )
    else:
        lines4 = ""
        lines5 = (
            f"layout = [\n"
            f"    breadcrumb,\n"
            f"    html.Section(\n"
            f'        id="{volume}",\n'
            f'        className="slicer-card",\n'
            f"        children=[\n"
            f'            html.Header(html.H2("View {description}")),\n'
            f'            html.Header(html.P("{filename}")),\n'
            f"            html.Div(\n"
            f"                children=[\n"
            f"                    slicer1.graph,\n"
            f"                    slicer1.slider,\n"
            f"                    *slicer1.stores,\n"
            f"                ],\n"
            f"            ),\n"
            f"        ],\n"
            f"    ),\n"
            f"]\n"
        )

    if img_data.at[i, "color1"] == "red" or img_data.at[i, "color1"] == "green":
        lines6 = (
            f"@callback(\n"
            f'    Output(slicer1.overlay_data.id, "data"),\n'
            f'    Input("{volume}", "children"),\n'
            f'    Input(slicer1.slider, "value"),\n'
            f")\n"
            f"def apply_levels(level, children):\n"
            f"    return slicer1.create_overlay_data(vol, colors)\n"
        )
    else:
        lines6 = ""

    if img_data.at[i, "color2"] == "red" or img_data.at[i, "color2"] == "green":
        lines7 = (
            f"@callback(\n"
            f'    Output(slicer2.overlay_data.id, "data"),\n'
            f'    Input("{volume}", "children"),\n'
            f'    Input(slicer2.slider, "value"),\n'
            f")\n"
            f"def apply_levels(level, children):\n"
            f"    return slicer2.create_overlay_data(vol2, colors)\n"
        )
    else:
        lines7 = ""

    with open(output_file, "a") as f:
        f.write(lines1)
        f.write(lines2)
        f.write(lines3)
        f.write(lines4)
        f.write(lines5)
        f.write(lines6)
        f.write(lines7)
