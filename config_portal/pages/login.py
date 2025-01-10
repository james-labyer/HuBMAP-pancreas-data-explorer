from dash import html, register_page

register_page(__name__, title="Log in")

layout = html.Div(html.P("Log in"))
