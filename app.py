# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd


app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


app.layout = dbc.Alert(
    "Hello, Bootstrap!", className="m-5"
)
px.set_mapbox_access_token("pk.eyJ1IjoibmFubzAxIiwiYSI6ImNraHVlYjQ4aDFidzYyeHBiemZlZ2d3d20ifQ.P6e2_ZATNHTAb6BWuadxFw")
df = pd.read_json(r'C:/Users/Nano/Documents/dash-project/Visu-group8/Dataset/fossils.json')
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", text="name",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)