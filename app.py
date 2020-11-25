# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import slicer as sl


app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


px.set_mapbox_access_token("pk.eyJ1IjoibmFubzAxIiwiYSI6ImNraHVlYjQ4aDFidzYyeHBiemZlZ2d3d20ifQ.P6e2_ZATNHTAb6BWuadxFw")
df = pd.read_json(r'Dataset/fossils.json')
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name = "name", hover_data=["old_latitude", "old_longitude"],
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)



df_fossil = pd.read_json(r'Dataset/fossils.json')
df_dino = pd.read_csv(r'Dataset/dinosaurs.csv')





divSlider = html.Div([
    dcc.Slider(
    id='slider',
    min=0,
    max=10,
    step=None,
    marks=sl.get_dictionary(df_dino) ,
    value=5
)])

#https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
divCards = html.Div([
    dbc.Card([
        dbc.CardImg(src=app.get_asset_url("Allosaurus.png"), top=True, style={"width": "200px", "height": "200px"}),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)


], id="dino-cards")

divMap = dcc.Graph(
        id='example-graph',
        figure=fig
    )

divTimeline = html.Div([html.P('Timeline')])
#Layout à modifier 

app.layout = html.Div(children=[
    html.H1(children='VISUDINO INGEN'),

    divSlider,

    html.Div(id='genom-list'),  
    divCards,
    divMap,
    divTimeline
    
])

@app.callback(
    dash.dependencies.Output('genom-list', 'children'),
    [dash.dependencies.Input('slider', 'value')])
def display_genus_buttons(value):
    dico = sl.get_dictionary(df_dino)
    picked_letter = dico[value]
    genom_list = sl.show_genoms(picked_letter, df_dino)

    genom_buttons = dbc.ButtonGroup([dbc.Button(name) for name in genom_list])
    print(genom_buttons)

    return genom_buttons


"""@app.callback(
    dash.dependencies.Output('dino-cards', 'children'),
    [dash.dependencies.Input('genom-list', 'value')])
def update_output(value):
    #TOD"""

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True, dev_tools_hot_reload=True)
    