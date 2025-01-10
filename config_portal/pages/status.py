import os
import sys
from dash import html, register_page

os.chdir("..")
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
os.chdir("./config_portal")


register_page(__name__)

layout = html.Div(html.P("Status"))
