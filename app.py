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


px.set_mapbox_access_token("pk.eyJ1IjoibmFubzAxIiwiYSI6ImNraHVlYjQ4aDFidzYyeHBiemZlZ2d3d20ifQ.P6e2_ZATNHTAb6BWuadxFw")
df = pd.read_json(r'Dataset/fossils.json')
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name = "name", hover_data=["old_latitude", "old_longitude"],
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)


divSlicer = html.Div([
    dcc.Slider(
    min=0,
    max=10,
    step=None,
    marks={
        0: '0 °F',
        3: '3 °F',
        5: '5 °F',
        7.65: '7.65 °F',
        10: '10 °F'
    },
    value=5
)], id = "slicer")

#https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
divCards = html.Div([html.P('Cards')])

divMap = dcc.Graph(
        id='example-graph',
        figure=fig
    )

divTimeline = html.Div([html.P('Timeline')])
#Layout à modifier 

app.layout = html.Div(children=[
    html.H1(children='VISUDINO INGEN'),

    divSlicer,  
    divCards,
    divMap,
    divTimeline
    
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)