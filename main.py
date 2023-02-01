# Nishad Govind Neelakandan
# Legal Assistant at White & Case LLP, Palo Alto
# Data current as of January 12, 2023
# Reverse Payment Choropleth

import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import dash
import dash_html_components as html
import dash_core_components as dcc

#Styles setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
darkgrey="#23262F"
lightgrey = "#444b5b"
pio.templates["WhiteCase"] = pio.templates["plotly_dark"]
pio.templates["WhiteCase"]['layout']['paper_bgcolor'] = lightgrey

app = dash.Dash(__name__)

# US District Courts GeoJSON map
with open("NeelakandanDistrictCourtMap.geojson", "r") as f:
    district_courts = json.load(f)
for feature in district_courts["features"]:
    feature["id"] = feature["properties"]["FID"]

#Read and store data
cache = {}
def filter_csv(file_path, year):
    if year in cache:
        return cache[year]
    df = pd.read_csv(file_path)
    df = df[df['year'] == year]
    cache[year] = df #new
    return df
file_path = "FID Test Data.csv"
year = 2001
df = filter_csv(file_path, year)

#Calibrate colorbar max values
setRangeMax = df["numCases"].max(axis=0)
if setRangeMax == 0:
    setRangeMax += 1
df["numberOfCases"] = df["numCases"]
df["id"] = df["FIDx"]

map_fig = px.choropleth(
    df,
    locations="id",
    geojson=district_courts,
    color="numberOfCases",
    color_continuous_scale=px.colors.sequential.Blues,
    hover_name="fidNAME",
    hover_data=["numberOfCases"],
    title="Reverse Payment Cases by District",
    range_color=(0, setRangeMax),
    template="WhiteCase",
    labels={"numberOfCases" : "Number of Cases"},
)
map_fig.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor=lightgrey,
)

map_fig.update_layout(
    template="WhiteCase",
    title=dict(x=0.5),
    font=dict(family="times")
)

app.layout = html.Div([
    html.Div(id='output-container'),
    dcc.Graph(id='dcc_Graph', figure=map_fig, style={'width': '95vw', 'height': '90vh'}),
    #html.Br(),
    html.Div(id='mapslider'),
    dcc.Slider(
        id='year-slider',
        min=2001,
        max=2003,
        step=1,
        value=2001,
        updatemode="drag",
        marks={year: str(year) for year in range(2001, 2023)},
        included=False,
        tooltip={"placement": "bottom", "always_visible": True},
    ),
])

@app.callback(
    [dash.dependencies.Output('output-container', 'children'), dash.dependencies.Output('dcc_Graph', 'figure')],
    [dash.dependencies.Input('year-slider', 'value')])
def update_CSVselection(value):
    year = value
    df = filter_csv(file_path, year)
    setRangeMax = df["numCases"].max(axis=0)
    if setRangeMax == 0:
        setRangeMax += 1
    df["numberOfCases"] = df["numCases"]
    df["id"] = df["FIDx"]

    map_fig = px.choropleth(
        df,
        locations="id",
        geojson=district_courts,
        color="numberOfCases",
        color_continuous_scale=px.colors.sequential.Blues,
        hover_name="fidNAME",
        hover_data=["numberOfCases"],
        title="Reverse Payment Cases by District",
        range_color=(0, setRangeMax),
        template="WhiteCase",
        labels={"numberOfCases": "Number of Cases", "id":"Federal Court ID"},
    )
    map_fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor=lightgrey,
    )
    map_fig.update_layout(
        template="WhiteCase",
        title=dict(x=0.5),
        font=dict(family="times")
    )
    #map_fig.update(data_frame = df)

    #map_fig = dcc.Graph(id='dcc_Graph', figure=map_fig, style={'width': '95vw', 'height': '90vh'})

    print(value)
    return [None, map_fig]

if __name__ == "__main__":
    app.run_server(debug=True)
