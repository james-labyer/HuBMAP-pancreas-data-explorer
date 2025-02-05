import os
import sys
import requests
import base64
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
import nh3
import shutil
import pandas as pd

# from config_portal.config_components import ui, validate
from config_components import ui, validate

from flask_login import current_user
from pathlib import Path

# os.chdir("..")
# if os.getcwd() not in sys.path:
#     sys.path.append(os.getcwd())
# os.chdir("./config_portal")

title = "Update Configuration"
MAX_EXCEL_SIZE = 1000000
MAX_IMG_SIZE = MAX_EXCEL_SIZE * 150
MAX_OBJ_SIZE = MAX_EXCEL_SIZE * 50

register_page(__name__, path="/", title=title)


confirm_title_msg = "Are you sure you want to update the title? This change will be immediately visible to the public."
confirm_si_block_msg = "Are you sure you want to update the tissue block and scientific metadata? This change will be immediately visible to the public."

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
                            "Update proteomics data",
                            ["For proteomics data file format, see example file:"],
                            "proteomics",
                            MAX_EXCEL_SIZE,
                        ),
                    ],
                    id="proteomics-data",
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
                                "Example .obj file of whole organ:",
                                "Example .obj file of tissue blocks:",
                            ],
                            "obj-files",
                            MAX_OBJ_SIZE,
                            # Add note about unsupported .obj features
                            summary_note="Not all .obj features are supported",
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
        content_type, content_string = list_of_contents.split(",")
        decoded = base64.b64decode(content_string)
        is_valid_type = validate.check_file_type(decoded, "excel")
        if is_valid_type[0]:
            done = validate.process_si_block_file(decoded, "si-block")
            if done[0]:
                return ui.success_toast(
                    "Metadata updated", "The file was uploaded successfully."
                )
            else:
                return ui.failure_toast("Metadata not updated", done[1])
            # return [list_of_contents[0:100]]
        else:
            return ui.failure_toast("Metadata not updated", is_valid_type[1])


# Proteomics
@callback(
    Output("proteomics-0-example-dl", "data"),
    Input("proteomics-0-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_proteomics_example(n_clicks):
    return dcc.send_file("examples/images-example.xlsx")


@callback(
    Output("output-proteomics-upload", "children"),
    Input("proteomics-upload", "contents"),
)
def update_proteomics_output(list_of_contents):
    if list_of_contents is not None:
        return [list_of_contents[0:16]]


@callback(
    Output("output-sci-images-upload", "children"),
    Input("sci-images-upload", "contents"),
    Input("sci-images-upload", "filename"),
)
def upload_sci_images(list_of_contents, filenames):
    # print(type(list_of_contents), file=sys.stdout, flush=True)
    if list_of_contents is not None:
        for i in range(len(list_of_contents)):
            print(list_of_contents[i][:100], file=sys.stdout, flush=True)
            if list_of_contents[i] == "":
                return ui.failure_toast(
                    "Image(s) not uploaded", "One or more files were too large."
                )
            content_type, content_string = list_of_contents[i].split(",")
            decoded = base64.b64decode(content_string)
            is_valid_type = validate.check_file_type(decoded, "image", filenames[i])
            if is_valid_type[0]:
                is_processed = validate.process_sci_image(decoded, filenames[i])
                if not is_processed[0]:
                    return ui.failure_toast("Image(s) not uploaded", is_processed[1])
            else:
                return ui.failure_toast("Image(s) not uploaded", is_valid_type[1])
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
    return dcc.send_file("examples/images-example.xlsx")


@callback(
    Output("obj-files-1-example-dl", "data"),
    Input("obj-files-1-example", "n_clicks"),
    prevent_initial_call=True,
)
def send_obj_example_2(n_clicks):
    return dcc.send_file("examples/images-example.xlsx")


@callback(
    Output("output-obj-files-upload", "children"),
    Input("obj-files-upload", "contents"),
)
def update_obj_files_output(list_of_contents):
    if list_of_contents is not None:
        return [list_of_contents[0:16]]


# Confirmation Modal
@callback(
    Output("update-modal-div", "children"),
    Input("title-publish", "n_clicks"),
    Input("si-block-publish", "n_clicks"),
    Input("sci-images-publish", "n_clicks"),
    prevent_initial_call=True,
)
def add_modal(title, si_block, sci_images):
    button_clicked = ctx.triggered_id
    if button_clicked == "title-publish":
        return ui.confirm_update_modal(confirm_title_msg, "title")
    elif button_clicked == "si-block-publish":
        return ui.confirm_update_modal(confirm_si_block_msg, "si-block")
    elif button_clicked == "sci-images-publish":
        return ui.confirm_update_modal(confirm_si_block_msg, "sci-images")
    return no_update


@callback(
    Output("confirm-update-modal", "is_open"),
    Output("update-status-div", "children"),
    [
        Input("confirm-update-title", "n_clicks"),
        Input("confirm-update-si-block", "n_clicks"),
        Input("confirm-update-sci-images", "n_clicks"),
        Input("cancel-update", "n_clicks"),
    ],
    [State("confirm-update-modal", "is_open"), State("title-input", "value")],
)
def toggle_modal(
    confirm_title, confirm_si_block, confirm_sci_images, cancel_update, is_open, value
):
    if confirm_title:
        return validate.update_title(value, is_open)
    elif confirm_si_block:
        # check if file has been processed
        # send request
        return validate.update_si_block(is_open)
    elif confirm_sci_images:
        return validate.update_sci_images(is_open)
    elif cancel_update:
        return not is_open, no_update
    else:
        return is_open, no_update
