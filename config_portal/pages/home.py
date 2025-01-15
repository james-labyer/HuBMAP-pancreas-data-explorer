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
from config_portal.components import ui, validate

os.chdir("..")
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
os.chdir("./config_portal")

title = "Update Configuration"
MAX_TITLE_LENGTH = 2048
MAX_EXCEL_SIZE = 1000000
MAX_IMG_SIZE = MAX_EXCEL_SIZE * 1000
MAX_OBJ_SIZE = MAX_EXCEL_SIZE * 50

register_page(__name__, path="/", title=title)


def update_title(value, is_open):
    if value:
        if len(value) > MAX_TITLE_LENGTH:
            return not is_open, ui.failure_alert(
                f"Title must be shorter than {MAX_TITLE_LENGTH} characters. Please try again."
            )
        else:
            clean_title = nh3.clean_text(value)
            r = requests.post(
                "http://localhost:8050/title",
                json={"title": clean_title},
                timeout=5,
            )
            if r.status_code == 204:
                return not is_open, ui.success_alert(
                    "The configuration has been updated. Refresh the public-facing app to see the changes."
                )
            else:
                return not is_open, ui.failure_alert(
                    f"Something went wrong. The public-facing app sent the following HTTP status code: {r.status_code}"
                )
    else:
        return not is_open, ui.failure_alert("Please provide a name.")


def update_si_block(is_open):
    block_data = {
        "file": (
            validate.FILE_DESTINATION["si-block"]["block-data"],
            open(validate.FILE_DESTINATION["si-block"]["block-data"], "rb"),
            "text/csv",
            {"Expires": "0"},
        )
    }

    r1 = requests.post(
        "http://localhost:8050/block-data",
        files=block_data,
        timeout=5,
    )

    if r1.status_code == 204:
        si_files = {
            "file": (
                validate.FILE_DESTINATION["si-block"]["si-files"],
                open(validate.FILE_DESTINATION["si-block"]["si-files"], "rb"),
                "text/csv",
                {"Expires": "0"},
            )
        }
        r2 = requests.post(
            "http://localhost:8050/si-files",
            files=si_files,
            timeout=5,
        )
        if r2.status_code == 204:
            return not is_open, ui.success_alert(
                "The configuration has been updated. Refresh the public-facing app to see the changes."
            )
        else:
            return not is_open, ui.failure_alert(
                f"Something went wrong. The public-facing app sent the following HTTP status code: {r2.status_code}"
            )

    else:
        return not is_open, ui.failure_alert(
            f"Something went wrong. The public-facing app sent the following HTTP status code: {r1.status_code}"
        )


confirm_title_msg = "Are you sure you want to update the title? This change will be immediately visible to the public."
confirm_si_block_msg = "Are you sure you want to update the tissue block and scientific metadata? This change will be immediately visible to the public."

pub_warning = dbc.Card(
    [
        dbc.CardBody(
            html.P(
                [
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    "Published data will be available to end users without a login",
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


layout = html.Div(
    [
        html.H2(title),
        pub_warning,
        html.Div(id="update-status-div"),
        html.Div(id="output-si-block-upload"),
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
                # is DL really useful for images?
                ui.make_upload_card(
                    "Update scientific images",
                    [
                        "Must be uploaded as a .zip file, no files over 1 GB. Can upload source files for download from website and .PNG images for display on website. Image names must match names in image metadata files. New images will replace existing images with the same name. See example file for details."
                    ],
                    "sci-images",
                    MAX_IMG_SIZE,
                    90,
                ),
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
        if is_valid_type:
            done = validate.process_si_block_file(decoded, "si-block")
            if done[0]:
                return ui.success_alert("The file was uploaded successfully.")
            else:
                return ui.failure_alert(done[1])
            # return [list_of_contents[0:100]]
        else:
            return ["Validation error"]


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
    prevent_initial_call=True,
)
def add_modal(title, si_block):
    button_clicked = ctx.triggered_id
    if button_clicked == "title-publish":
        return ui.confirm_update_modal(confirm_title_msg, "title")
    elif button_clicked == "si-block-publish":
        return ui.confirm_update_modal(confirm_si_block_msg, "si-block")
    return no_update


@callback(
    Output("confirm-update-modal", "is_open"),
    Output("update-status-div", "children"),
    [
        Input("confirm-update-title", "n_clicks"),
        Input("confirm-update-si-block", "n_clicks"),
        Input("cancel-update", "n_clicks"),
    ],
    [State("confirm-update-modal", "is_open"), State("title-input", "value")],
)
def toggle_modal(confirm_title, confirm_si_block, cancel_update, is_open, value):
    if confirm_title:
        return update_title(value, is_open)
    elif confirm_si_block:
        # check if file has been processed
        # send request
        return update_si_block(is_open)
    elif cancel_update:
        return not is_open, no_update
    else:
        return is_open, no_update
