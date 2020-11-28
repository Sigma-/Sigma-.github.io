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
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import time
import plotly.graph_objects as go


app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.config.suppress_callback_exceptions = True

px.set_mapbox_access_token("pk.eyJ1IjoibmFubzAxIiwiYSI6ImNraHVlYjQ4aDFidzYyeHBiemZlZ2d3d20ifQ.P6e2_ZATNHTAb6BWuadxFw")
df = pd.read_json(r'Dataset/fossils.json')
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name = "name", hover_data=["old_latitude", "old_longitude"],
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=1)



df_fossil = pd.read_json(r'Dataset/fossils.json')
df_dino = pd.read_csv(r'Dataset/dinosaurs.csv')

df_dino_names = [dinoname for dinoname in df_dino['dinosaur']]



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
#divCards = 


divMap = dcc.Graph(
        id='dino-map',
        figure = fig
    )

divTimeline = html.Div([html.P('Timeline')])
#Layout à modifier 

app.layout = html.Div(children=[
    html.H1(children='VISUDINO INGEN'),

    divSlider,

    html.Div(id='genom-list'),
    dcc.Loading(
        id="loading-1",
        type="circle",
        children = html.Div(id='dino-cards')
    ),
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
    
    print(sl.mapping_multiple_genom_to_dino(genom_list))

    genom_buttons = dbc.Container(
    [
        dbc.RadioItems(
            options=[{"label": v , "value" : v} for v in genom_list],
            id="genom-selector",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
        ),
        html.P(id="output"),
    ],
    className="p-3",
)
    
    return genom_buttons

@app.callback(dash.dependencies.Output("dino-cards", "children"), [dash.dependencies.Input("genom-selector", "value")])
def return_value(value):
    if value != None: 
        index_of_genom = df_dino.set_index("dinosaur").index.get_loc(f"{value}")
        divCards =  dbc.Card([
            dbc.CardImg(src=app.get_asset_url(f"{value}.png"), top=True, style={"width": "200px", "height": "200px"}),
            dbc.CardBody(
                [
                    html.H4(f"{value}", className="card-title"),
                    html.P(
                        f"Zone : {df_dino['zone'][index_of_genom]}",
                        className="card-text",
                    ),
                    html.P(
                        f"Diet : {df_dino['diet'][index_of_genom]}",
                        className="card-text",
                    ),
                    html.P(
                        f"Size : {df_dino['size'][index_of_genom]}",
                        className="card-text",
                    ),
                    html.P(
                        f"Weight : {df_dino['weight'][index_of_genom]}",
                        className="card-text",
                    ),
                    html.P(
                        f"Speed : {df_dino['speed'][index_of_genom]}",
                        className="card-text",
                    ),
    
                    dbc.Button("Go somewhere", color="primary"),
                ]
                ),
            ],
            style={"width": "18rem"},
            )
        time.sleep(1)
        return divCards


@app.callback(dash.dependencies.Output("dino-map", "figure"), [dash.dependencies.Input("genom-selector", "value")])
def change_map(value):
    if value == None : 
        fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name = "name", hover_data=["old_latitude", "old_longitude"],
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=1)
        fig.update_layout(transition_duration=500)
        return fig
    else:    
        fig = px.scatter_mapbox(sl.mapping_genome_to_dino(value), lat="latitude", lon="longitude", hover_name = "name", hover_data=["old_latitude", "old_longitude"],
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=1)
        fig.update_layout(transition_duration=500)
        return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True, dev_tools_hot_reload=True)

