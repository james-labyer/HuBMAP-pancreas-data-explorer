from dash import (
    html,
    register_page,
    dcc,
    Output,
    Input,
    State,
    callback,
    no_update,
    ctx,
)
import dash_bootstrap_components as dbc
from config_components import ui, validate
from flask_login import current_user
import sys

title = "Update Configuration"
MAX_EXCEL_SIZE = 150000000
MAX_IMG_SIZE = MAX_EXCEL_SIZE  # * 150
MAX_OBJ_SIZE = MAX_EXCEL_SIZE  # * 50

register_page(__name__, path="/", title=title)


pub_warning = dbc.Card(
    [
        dbc.CardBody(
            html.P(
                [
                    html.I(className="fa-solid fa-triangle-exclamation me-2"),
                    "Published data will be available to end users without a login",
                ],
            ),
        ),
    ],
    color="warning",
    inverse=True,
    class_name="form-card",
)

login_warning = dbc.Card(
    [
        dbc.CardBody(
            html.P(
                [
                    html.I(className="fa-solid fa-triangle-exclamation me-2"),
                    "Please ",
                    dcc.Link("log in", href="/login", className="link--warning"),
                    " to continue",
                ],
            ),
        ),
    ],
    color="warning",
    inverse=True,
    class_name="form-card",
)

title_form = dbc.Card(
    [
        dbc.CardHeader(html.H4("Update app name", className="upload-card-title")),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Label("Name: ", html_for="title-input", width="auto"),
                        dbc.Col(dbc.Input(type="text", id="title-input"), width=True),
                        dbc.Col(
                            dbc.Button("Publish", id="title-publish", color="warning"),
                            width="auto",
                        ),
                    ],
                    align="center",
                    justify="between",
                ),
            ]
        ),
    ],
    color="light",
    class_name="form-card",
)


def layout(**kwargs):
    if not current_user.is_authenticated:
        return login_warning
    else:
        return html.Div(
            [
                dcc.Location(id="config-url"),
                html.H2(title),
                pub_warning,
                html.Div(id="update-status-div"),
                html.Section(
                    [
                        title_form,
                        html.Div(id="update-modal-div"),
                    ],
                    id="app-settings",
                ),
                html.Section(
                    [
                        ui.make_upload_card(
                            "Update tissue block and scientific image metadata",
                            [
                                "For tissue block and scientific metadata file format, see example file:"
                            ],
                            "si-block",
                            MAX_EXCEL_SIZE,
                        ),
                        html.Div(id="output-si-block-upload"),
                    ],
                    id="block-metadata",
                ),
                html.Section(
                    [
                        ui.make_upload_card(
                            "Update spatial map data",
                            [
                                "Spatial map data file format:",
                                "Downloads file format:",
                            ],
                            "spatial-map",
                            MAX_EXCEL_SIZE,
                            accordion=True,
                            acc_notes=[
                                [
                                    "Upload Requirements",
                                    html.Ul(
                                        [
                                            html.Li("No files over 150 MB."),
                                            html.Li(
                                                [
                                                    "Spatial map data must be in a file named ",
                                                    html.Strong(
                                                        "spatial-map-data.xlsx"
                                                    ),
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    "Downloads data must be in a file named ",
                                                    html.Strong("downloads.xlsx"),
                                                ]
                                            ),
                                        ]
                                    ),
                                    # "No files over 150 MB. Spatial map data must be in a file named spatial-map-data.xlsx, and downloads data must be in a file named downloads.xlsx.",
                                ],
                                [
                                    "Supported File Types",
                                    ", ".join(validate.VALID_EXTS["excel/vol"]),
                                ],
                                [
                                    "Spatial Map Data Requirements",
                                    html.Ul(
                                        [
                                            html.Li(
                                                "The spatial-map-data.xlsx file must include all of the tabs included in the example workbook"
                                            ),
                                            html.Li(
                                                "All of the columns in the example workbook are required except for the value columns from Column I-O in the points_data worksheet"
                                            ),
                                            html.Li(
                                                "The value columns are optional: provide as many as you like and name them as you see fit"
                                            ),
                                        ]
                                    ),
                                ],
                                [
                                    "Downloads Requirements",
                                    html.Ul(
                                        [
                                            html.Li(
                                                "Filenames in downloads.xlsx must be unique and must match the name of a file provided to this interface exactly"
                                            ),
                                            html.Li(
                                                "Do not use any characters besides a-z, A_Z, 0-9, -, _, and whitespace in the download filenames"
                                            ),
                                            html.Li(
                                                "Files with the same block will be displayed on the same page"
                                            ),
                                            html.Li(
                                                "New downloads.xlsx entries will be added to existing downloads.xlsx entries from previous uploads"
                                            ),
                                            html.Li(
                                                "If you upload any other file with a name that matches a previously uploaded file exactly, it will replace the old version of that file"
                                            ),
                                        ]
                                    ),
                                ],
                            ],
                            upload_multiple=True,
                        ),
                        dcc.Loading(html.Div(id="output-spatial-map-upload")),
                    ],
                    id="spatial-map-data",
                ),
                html.Section(
                    [
                        ui.make_upload_card(
                            "Update scientific images",
                            [],
                            "sci-images",
                            MAX_IMG_SIZE,
                            90,
                            example=False,
                            accordion=True,
                            acc_notes=[
                                [
                                    "Upload Requirements",
                                    "No files over 150 MB. Can upload source files for download from website and .PNG images for display on website. Source file names must match names in image metadata file exactly. PNG image file names must follow the format described in Image Names. New images will replace existing images with the same name.",
                                ],
                                [
                                    "Supported File Types",
                                    ", ".join(validate.VALID_EXTS["image"]),
                                ],
                                [
                                    "Image Names",
                                    "PNG image names must be of the following format: {Source file name}_C{Channel number, starting at zero}{sequence number, starting at zero and padded with zeroes to four digits}. Example: P1_4A2_image_stack_C10001.png .",
                                ],
                            ],
                            upload_multiple=True,
                        ),
                        dcc.Loading(html.Div(id="output-sci-images-upload")),
                    ],
                    id="sci-images",
                ),
                html.Section(
                    [
                        ui.make_upload_card(
                            "Update 3D model files",
                            [
                                "Example summary file:",
                                "Example .obj file of whole organ:",
                                "Example .obj file of a tissue block within the organ:",
                            ],
                            "obj-files",
                            MAX_OBJ_SIZE,
                            accordion=True,
                            acc_notes=[
                                [
                                    "Upload Instructions",
                                    "No files over 150 MB. Please upload model files in .obj format and a summary file called obj-files.xlsx that lists the model files",
                                ],
                                [
                                    "Summary File",
                                    html.Ul(
                                        [
                                            html.Li(
                                                "Please name the file obj-files.xlsx"
                                            ),
                                            html.Li(
                                                "Files with the same value in the Organ column will be displayed together in the same figure"
                                            ),
                                            html.Li(
                                                "When a file's Name value matches a tissue block exactly, information about that tissue block will be displayed to the user when they click on that element"
                                            ),
                                            html.Li("Specify color with a hex value"),
                                            html.Li(
                                                "Opacity is a number between 0 and 1"
                                            ),
                                        ]
                                    ),
                                ],
                                [
                                    "OBJ Files",
                                    html.Ul(
                                        [
                                            html.Li(
                                                "The app does not use texture coordinates, vertex normals, or parameter space vertices to display the models, so please only include v and f tags to reduce file size"
                                            ),
                                            html.Li("Model file names must be unique"),
                                        ]
                                    ),
                                ],
                            ],
                            upload_multiple=True,
                        ),
                    ],
                    id="obj-files",
                ),
            ]
        )


# Scientific images metadata
@callback(
    Output("si-block-0-example-dl", "data"),
    Input("si-block-0-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_images_example(n_clicks):
    return dcc.send_file("examples/images-example.xlsx")


@callback(
    Output("output-si-block-upload", "children"),
    Input("si-block-upload", "contents"),
    Input("si-block-upload", "filename"),
)
def update_si_block_output(list_of_contents, filename):
    if list_of_contents is not None:
        upload_succeeded = validate.upload_content(
            list_of_contents,
            filename,
            "excel",
            validate.process_si_block_file,
            "si-block",
        )
        if not upload_succeeded[0]:
            return ui.failure_toast("Metadata not updated", upload_succeeded[1])
        else:
            return ui.success_toast(
                "Metadata updated", "The file was uploaded successfully."
            )


# Spatial map
@callback(
    Output("spatial-map-0-example-dl", "data"),
    Input("spatial-map-0-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_spatial_map_example(n_clicks):
    return dcc.send_file("examples/spatial-map-data.xlsx")


@callback(
    Output("spatial-map-1-example-dl", "data"),
    Input("spatial-map-1-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_spatial_map_downloads_example(n_clicks):
    return dcc.send_file("examples/downloads.xlsx")


@callback(
    Output("output-spatial-map-upload", "children"),
    Input("spatial-map-upload", "contents"),
    Input("spatial-map-upload", "filename"),
)
def upload_spatial_map(list_of_contents, filenames):
    if list_of_contents is not None:
        files_iter = [x for x in range(len(list_of_contents))]
        # make sure downloads.xlsx gets processed first if included
        if len(list_of_contents) > 1 and "downloads.xlsx" in filenames:
            # get index to use for contents and filenames
            idx = filenames.index("downloads.xlsx")
            # call upload_content
            upload_succeeded = validate.upload_content(
                list_of_contents[idx],
                filenames[idx],
                "excel/vol",
                validate.upload_spatial_map_data,
                filenames[idx],
            )
            if not upload_succeeded[0]:
                return ui.failure_toast(
                    "Spatial map data not uploaded", upload_succeeded[1]
                )
            # delete that index from files_iter so it doesn't get re-processed
            files_iter.remove(idx)
        for i in files_iter:
            upload_succeeded = validate.upload_content(
                list_of_contents[i],
                filenames[i],
                "excel/vol",
                validate.upload_spatial_map_data,
                filenames[i],
            )
            if not upload_succeeded[0]:
                return ui.failure_toast(
                    "Spatial map data not uploaded", upload_succeeded[1]
                )
            else:
                return ui.success_toast(
                    "Spatial map data uploaded", "The files were uploaded successfully."
                )


@callback(
    Output("output-sci-images-upload", "children"),
    Input("sci-images-upload", "contents"),
    Input("sci-images-upload", "filename"),
)
def upload_sci_images(list_of_contents, filenames):
    if list_of_contents is not None:
        for i in range(len(list_of_contents)):
            upload_succeeded = validate.upload_content(
                list_of_contents[i],
                filenames[i],
                "image",
                validate.process_sci_image,
                filenames[i],
            )
            if not upload_succeeded[0]:
                return ui.failure_toast("Image(s) not uploaded", upload_succeeded[1])
        return ui.success_toast(
            "Images uploaded", "The files were uploaded successfully."
        )


# 3D Models
@callback(
    Output("obj-files-0-example-dl", "data"),
    Input("obj-files-0-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_obj_example_1(n_clicks):
    return dcc.send_file("examples/obj-files.xlsx")


@callback(
    Output("obj-files-1-example-dl", "data"),
    Input("obj-files-1-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_obj_example_2(n_clicks):
    return dcc.send_file("examples/images-example.xlsx")


@callback(
    Output("obj-files-2-example-dl", "data"),
    Input("obj-files-2-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_obj_example_3(n_clicks):
    return dcc.send_file("examples/images-example.xlsx")


@callback(
    Output("output-obj-files-upload", "children"),
    Input("obj-files-upload", "contents"),
    Input("obj-files-upload", "filename"),
)
def update_obj_files_output(list_of_contents, filenames):
    if list_of_contents is not None:
        for i in range(len(list_of_contents)):
            upload_succeeded = validate.upload_content(
                list_of_contents[i],
                filenames[i],
                "3d",
                validate.process_obj_files,
                filenames[i],
            )
            print("upload_succeeded:", upload_succeeded, file=sys.stdout, flush=True)
            if not upload_succeeded[0]:
                return ui.failure_toast("Model files not uploaded", upload_succeeded[1])
        return ui.success_toast(
            "Model files uploaded", "The files were uploaded successfully."
        )


# Confirmation Modal
@callback(
    Output("update-modal-div", "children"),
    Input("title-publish", "n_clicks"),
    Input("si-block-publish", "n_clicks"),
    Input("sci-images-publish", "n_clicks"),
    Input("spatial-map-publish", "n_clicks"),
    Input("obj-files-publish", "n_clicks"),
    prevent_initial_call=True,
)
def add_modal(title, si_block, sci_images, spatial_map, obj_files):
    button_clicked = ctx.triggered_id
    publish_buttons = {
        "title-publish": [
            "title",
            "Are you sure you want to update the title? This change will be immediately visible to the public.",
        ],
        "si-block-publish": [
            "si-block",
            "Are you sure you want to update the tissue block and scientific metadata? This change will be immediately visible to the public.",
        ],
        "sci-images-publish": [
            "sci-images",
            "Are you sure you want to update the scientific images? This change will be visible to the public once you restart the display app.",
        ],
        "spatial-map-publish": [
            "spatial-map",
            "Are you sure you want to update the spatial map data? This change will be immediately visible to the public.",
        ],
        "obj-files-publish": [
            "obj-files",
            "Are you sure you want to update the 3D model files? This change will be immediately visible to the public.",
        ],
    }

    if button_clicked in publish_buttons:
        return ui.confirm_update_modal(
            publish_buttons[button_clicked][1], publish_buttons[button_clicked][0]
        )
    else:
        return no_update


@callback(
    Output("confirm-update-modal", "is_open"),
    Output("update-status-div", "children"),
    [
        Input("confirm-update-title", "n_clicks"),
        Input("confirm-update-si-block", "n_clicks"),
        Input("confirm-update-sci-images", "n_clicks"),
        Input("confirm-update-spatial-map", "n_clicks"),
        Input("confirm-update-obj-files", "n_clicks"),
        Input("cancel-update", "n_clicks"),
    ],
    [State("confirm-update-modal", "is_open"), State("title-input", "value")],
)
def toggle_modal(
    confirm_title,
    confirm_si_block,
    confirm_sci_images,
    confirm_spatial_map,
    confirm_obj_files,
    cancel_update,
    is_open,
    value,
):
    if confirm_title:
        return validate.update_title(value, is_open)
    elif confirm_si_block:
        return validate.update_si_block(is_open)
    elif confirm_sci_images:
        return validate.update_sci_images(is_open)
    elif confirm_spatial_map:
        return validate.publish_spatial_map_data(is_open)
    elif confirm_obj_files:
        return validate.publish_obj_files(is_open)
    elif cancel_update:
        return not is_open, no_update
    else:
        return is_open, no_update
