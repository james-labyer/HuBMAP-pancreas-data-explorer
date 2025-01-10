import os
import sys
import requests
from dash import html, register_page, dcc, Output, Input, State, callback, no_update
import dash_bootstrap_components as dbc
import nh3

os.chdir("..")
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
os.chdir("./config_portal")

title = "Update Configuration"
MAX_TITLE_LENGTH = 2048

register_page(__name__, path="/", title=title)


def confirm_modal(message, update_id):
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Publish Update")),
            dbc.ModalBody(message),
            dbc.ModalFooter(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "Publish",
                                    id=update_id,
                                    className="ms-auto",
                                    color="light",
                                    n_clicks=0,
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Close",
                                    id="cancel-update",
                                    className="ms-auto",
                                    n_clicks=0,
                                ),
                                width="auto",
                            ),
                        ]
                    )
                ]
            ),
        ],
        id="confirm-update-modal",
        is_open=True,
    )


def failure_alert(message):
    return dbc.Alert(
        message,
        id="failure-alert",
        is_open=True,
        dismissable=True,
        fade=False,
        color="danger",
    )


confirm_title_msg = "Are you sure you want to update the title? This change will be immediately visible to the public."

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
        dbc.CardHeader(html.H4("Update app name")),
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

success_alert = dbc.Alert(
    "The configuration has been updated. Refresh the public-facing app to see the changes.",
    id="success-alert",
    is_open=True,
    duration=4000,
    dismissable=True,
    fade=False,
    color="success",
)


layout = html.Div(
    [
        html.H2(title),
        pub_warning,
        html.Section(
            [
                title_form,
                html.Div(id="update-modal-div"),
                html.Div(id="update-status-div"),
            ],
            id="app-settings",
        ),
    ]
)


@callback(
    Output("update-modal-div", "children"),
    Input("title-publish", "n_clicks"),
    prevent_initial_call=True,
)
def add_modal(n1):
    if n1 > 0:
        return confirm_modal(confirm_title_msg, "confirm-update-title")
    return no_update


@callback(
    Output("confirm-update-modal", "is_open"),
    Output("update-status-div", "children"),
    [
        Input("confirm-update-title", "n_clicks"),
        Input("cancel-update", "n_clicks"),
    ],
    [State("confirm-update-modal", "is_open"), State("title-input", "value")],
)
def toggle_modal(confirm_title, cancel_update, is_open, value):
    if confirm_title:
        if value:
            if len(value) > MAX_TITLE_LENGTH:
                return not is_open, failure_alert(
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
                    return not is_open, success_alert
                else:
                    return not is_open, failure_alert(
                        f"Something went wrong. The public-facing app sent the following HTTP status code: {r.status_code}"
                    )
        else:
            return not is_open, no_update
    elif cancel_update:
        return not is_open, no_update
    else:
        return is_open, no_update


# @callback(
#     Output("confirm-update-modal", "is_open"),
#     [
#         Input("title-publish", "n_clicks"),
#         Input("confirm-update", "n_clicks"),
#         Input("cancel-update", "n_clicks"),
#     ],
#     [State("confirm-update-modal", "is_open")],
# )
# def toggle_modal(n1, n2, n3, is_open):
#     if n1 or n2 or n3:
#         return not is_open
#     return is_open


# @callback(
#     Output("container-button-basic", "children"),
#     Input("title-publish", "n_clicks"),
#     State("title-input", "value"),
#     prevent_initial_call=True,
# )
# def update_output(n_clicks, value):
#     r = requests.post("http://localhost:8050/title", json={"title": value})
#     if r.status_code == 204:
#         return dbc.Alert(
#             "The configuration has been updated. Refresh the public-facing app to see the changes.",
#             id="title-success-alert",
#             is_open=True,
#             duration=10000,
#             dismissable=True,
#             fade=False,
#             color="success",
#         )
#     else:
#         return dbc.Alert(
#             f"Something went wrong. The public-facing app sent the following HTTP status code: {r.status_code}",
#             id="title-failure-alert",
#             is_open=True,
#             dismissable=True,
#             fade=False,
#             color="danger",
#         )
