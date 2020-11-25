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



df_fossil = pd.read_json(r'Dataset/fossils.json')
df_dino = pd.read_csv(r'Dataset/dinosaurs.csv')

# print(df_fossil.head())
# print(df_dino.head())
# print(df_dino.columns)
# print(df_fossil.columns)

first_letter = df_dino['dinosaur'].str[:1]

first_letterlist = []
first_letterlist = first_letter.unique()

slicer_dictionary = {}
keys = range(len(first_letterlist))

for i in keys:
    slicer_dictionary[i] = first_letterlist[i]

print(slicer_dictionary)


#print(f"First letter list: {first_letterlist}")
#print(f"first letter: {first_letter}")
print(f"Slicer dictionart: {slicer_dictionary}")


picked_letter = 'a'
capitalized_letter = picked_letter.upper()
print(F"Capitalized letter: {capitalized_letter}")
genom = df_dino.loc[first_letter == picked_letter]
genom_list = genom['dinosaur'].unique()

print(genom_list)
genom_picked = genom_list[0]
print("genom_picked")

def mapping_genome_to_dino(genom_picked):

    for i in range(0,len(df_fossil)):
        fossil_entire_name = df_fossil['name'][i]
        fossil_first_name = df_fossil['name'][i].split()[0].lower()
        if genom_picked == fossil_first_name:
            print(fossil_entire_name)


 
mapping_genome_to_dino(genom_picked)



divSlicer = html.Div([
    dcc.Slider(
    min=0,
    max=10,
    step=None,
    marks=slicer_dictionary ,
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