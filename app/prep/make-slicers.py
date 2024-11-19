import pandas as pd

blocks = [7, 14, 19]

for m in range(len(blocks)):
    img_data = pd.read_csv(f"./prep/imgs1-{blocks[m]}A.csv")

    for i in range(img_data.shape[0]):
        fname = img_data.at[i, "fname"]
        volume = img_data.at[i, "volume"]
        description = img_data.at[i, "description"]
        filename = img_data.at[i, "filename"]
        dname = img_data.at[i, "download"]
        folder = f"assets/optical-clearing-czi/P1-{blocks[m]}A/"
        dataset = f"P1-{blocks[m]}A optical clearing"
        output_file = f"./prep/output/{fname}.py"
        slices = img_data.at[i, "slices"]
        channel_colors = []
        for n in range(img_data.at[i, "channels"]):
            channel_colors.append(img_data.at[i, f"color{n + 1}"])

        # print("block:", blocks[m], "row:", i, "channel colors:", channel_colors)
        lines0 = "import dash_bootstrap_components as dbc\n" "import logging\n"

        if img_data.at[i, "format"] == "czi":
            lines1 = (
                "from dash import html, dcc, callback, Input, Output, get_app, register_page\n"
                "from dash_slicer import VolumeSlicer\n"
                f"from bioio import BioImage\n"
                f"import bioio_czi\n"
                f"\n"
                f'slices_img = BioImage("{folder}{filename}", reader=bioio_czi.Reader)\n'
                f"vols = slices_img.data[0]\n"
            )
        elif img_data.at[i, "format"] == "avi":
            lines1 = (
                "from dash import html, dcc, callback, Input, Output, register_page\n"
                "from PIL import Image\n"
                "\n"
            )
        elif img_data.at[i, "channels"] > 1 and img_data.at[i, "slices"] > 1:
            lines1 = (
                "from dash import html, dcc, callback, Input, Output, get_app, register_page\n"
                "from dash_slicer import VolumeSlicer\n"
                f"import numpy as np\n"
                f"import imageio.v3 as iio\n"
                f"\n"
                f"im = iio.imread(\n"
                f"'{folder}{filename}'\n"
                f")\n"
            )
            for k in range(img_data.at[i, "channels"]):
                lines1 += f"temp{k} = []\n"

            slices = img_data.at[i, "slices"]
            lines1 += f"for i in range({slices}):\n"
            for k in range(img_data.at[i, "channels"]):
                lines1 += f"    temp{k}.append(im[i][{k}])\n"
            lines1 += "vols = []\n"
            for k in range(img_data.at[i, "channels"]):
                lines1 += f"vols.append(np.array(temp{k}))\n"

        else:
            lines1 = (
                "from dash import html, dcc, callback, Input, Output, get_app, register_page\n"
                "from dash_slicer import VolumeSlicer\n"
                f"import numpy as np\n"
                f"import imageio.v3 as iio\n"
                f"\n"
                f"im = iio.imread(\n"
                f"'{folder}{filename}'\n"
                f")\n"
                f"vols = []\n"
            )
            for j in range(img_data.at[i, "channels"]):
                lines1 += f"vols.append(np.expand_dims(im[{j}], axis=0))\n"

        lines2 = (
            f"txt2 =register_page(\n"
            f"    __name__,\n"
            f'    path="/p1-{blocks[m]}a-optical-clearing/{volume.lower()}",\n'
            f'    title="{description}",\n'
            f")\n"
        )

        lines3 = ""

        if "green" in channel_colors:
            lines3 += 'greens = ["#{:02x}{:02x}{:02x}".format(0, i, 0) for i in range(0, 256, 1)]\n'
        if "red" in channel_colors:
            lines3 += 'reds = ["#{:02x}{:02x}{:02x}".format(i, 0, 0) for i in range(0, 256, 1)]\n'

        lines4 = ""

        if img_data.at[i, "format"] != "avi":
            for j in range(img_data.at[i, "channels"]):
                lines4 += f"vol{j} = vols[{j}]\n"
                lines4 += f"slicer{j} = VolumeSlicer(get_app(), vol{j})\n"
                lines4 += f'slicer{j}.graph.config["scrollZoom"] = False\n'
                lines4 += "logging.debug(\n"
                lines4 += f"    f'Added slicer{j} with {{slicer{j}.nslices}} slices to {volume}'\n"
                lines4 += ")\n"

        lines5 = (
            f"layout = [\n"
            f"    html.Section(\n"
            f'        id="{volume}",\n'
            f"        children=[\n"
            f'            html.Header(html.H2("View {description}")),\n'
            f'            html.P("{dname}"),\n'
            f"            html.Div(\n"
            f"                [\n"
        )

        lines6 = ""
        if img_data.at[i, "format"] == "avi":
            lines6 += "                    dbc.Card(\n"
            lines6 += "                        [\n"
            lines6 += "                            html.Div(\n"
            lines6 += f'                                id="{volume}-slider-output",\n'
            lines6 += '                               className="custom-slicer-div",\n'
            lines6 += "                           ),\n"
            lines6 += "                           dbc.CardBody(\n"
            lines6 += f'                                dcc.Slider(1, {slices}, 1, value=1, id="{volume}-slider"),\n'
            lines6 += "                            ),\n"
            lines6 += "                        ],\n"
            lines6 += '                        class_name="slicer-card",\n'
            lines6 += "                    ),\n"
        else:
            for j in range(img_data.at[i, "channels"]):
                if img_data.at[i, f"loading{j+1}"] == "no":
                    lines6 += "                    dbc.Card(\n"
                    lines6 += "                        dbc.CardBody(\n"
                    lines6 += "                             children=[\n"
                    lines6 += f"                                slicer{j}.graph,\n"
                    lines6 += f"                                slicer{j}.slider,\n"
                    lines6 += f"                                *slicer{j}.stores,\n"
                    lines6 += "                            ],\n"
                    lines6 += '                            className="slicer",\n'
                    lines6 += "                        ),\n"
                    lines6 += '                        class_name="slicer-card",\n'
                    lines6 += "                    ),\n"
                else:
                    lines6 += "                    dcc.Loading(\n"
                    lines6 += "                        [\n"
                    lines6 += "                            dbc.Card(\n"
                    lines6 += "                                dbc.CardBody(\n"
                    lines6 += "                                    children=[\n"
                    lines6 += (
                        f"                                        slicer{j}.graph,\n"
                    )
                    lines6 += (
                        f"                                        slicer{j}.slider,\n"
                    )
                    lines6 += (
                        f"                                        *slicer{j}.stores,\n"
                    )
                    lines6 += "                                    ],\n"
                    lines6 += (
                        '                                    className="slicer",\n'
                    )
                    lines6 += "                                ),\n"
                    lines6 += (
                        '                                class_name="slicer-card",\n'
                    )
                    lines6 += "                            ),\n"
                    lines6 += "                        ],\n"
                    lines6 += "                        style={\n"
                    lines6 += '                            "visibility": "visible",\n'
                    lines6 += '                            "backgroundColor": "transparent",\n'
                    lines6 += '                            "opacity": 0.5,\n'
                    lines6 += "                        },\n"
                    lines6 += '                        type="dot",\n'
                    lines6 += (
                        '                        parent_className="loader-wrapper",\n'
                    )
                    lines6 += "                    ),\n"

        lines7 = (
            "                ]\n"
            "            ),\n"
            "            html.Div(\n"
            "                children=[\n"
            '                    html.H2("Download file", className="download-header"),\n'
        )

        if img_data.at[i, "format"] == "avi":
            lines8 = (
                f"                    dbc.Button(\n"
                f'                        "Download",\n'
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
        else:
            lines8 = (
                f"                    html.P(\n"
                f'                        "The easiest way to open this file is to use Fiji with the Bio-Formats plugin installed."\n'
                f"                    ),\n"
                f"                    dbc.Button(\n"
                f'                        "Download",\n'
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

        lines9 = ""
        if img_data.at[i, "format"] == "avi":
            lines9 += "@callback(\n"
            lines9 += f'    Output("{volume}-slider-output", "children"),\n'
            lines9 += f'    Input("{volume}-slider", "value"),\n'
            lines9 += ")\n"
            lines9 += "def update_pic(value):\n"
            lines9 += "    val = value - 1\n"
            lines9 += '    val_str = f"{val:04}"\n'
            lines9 += "    pic = Image.open(\n"
            lines9 += f'        f"{folder}/{filename}/{filename}{{val_str}}.png"\n'
            lines9 += "    )\n"
            lines9 += '    return html.Img(src=pic, className="custom-slicer-img")\n'
            lines9 += "\n"
        else:
            for j in range(img_data.at[i, "channels"]):
                if (
                    img_data.at[i, f"color{j+1}"] == "red"
                    or img_data.at[i, f"color{j+1}"] == "green"
                ):
                    lines9 += "@callback(\n"
                    lines9 += f'    Output(slicer{j}.overlay_data.id, "data"),\n'
                    lines9 += f'    Input("{volume}", "children"),\n'
                    lines9 += f'    Input(slicer{j}.slider, "value"),\n'
                    lines9 += ")\n"
                    lines9 += f"def apply_overlay{j}(level, children):\n"
                    lines9 += f'    logging.info("Creating overlay on {volume}")\n'
                    if channel_colors[j] == "red":
                        lines9 += (
                            f"    return slicer{j}.create_overlay_data(vol{j}, reds)\n"
                        )
                        lines9 += "\n"
                    elif channel_colors[j] == "green":
                        lines9 += f"    return slicer{j}.create_overlay_data(vol{j}, greens)\n"
                        lines9 += "\n"

        lines10 = (
            f"@callback(\n"
            f'    Output("download-{volume}", "data"),\n'
            f'    Input("btn-download-{volume}", "n_clicks"),\n'
            f"    prevent_initial_call=True,\n"
            f")\n"
            f"def download_file(n_clicks):\n"
            f"    logging.info(\n"
            f'        "Sending {dname}"\n'
            f"    )\n"
            f"    return dcc.send_file(\n"
            f'        "{folder}{dname}"\n'
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
            f.write(lines9)
            f.write(lines10)
