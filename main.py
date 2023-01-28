# Nishad Govind Neelakandan
# Legal Assistant at White & Case LLP, Palo Alto
# Data current as of January 28, 2023
# Reverse Payment Choropleth


import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

district_courts = json.load(open("US_District_Court_Jurisdictions.geojson", "r"))

court_id_map = {}
for feature in district_courts["features"]:
    feature["id"] = feature["properties"]["FID"]

rowSelection = 89
twothousandone = rowSelection
twothousandtwo = range(1,89)
twothousandthree = range(1,177)
twothousandfour = range (1, 265)
df = pd.read_csv("FID Test Data.csv", skiprows=twothousandtwo,nrows=rowSelection)
setRangeMax = df["numCases"].max(axis=0)
if setRangeMax == 0:
    setRangeMax += 1
print(setRangeMax)

df["numberOfCases"] = df["numCases"]
df["id"]=df["FIDx"]

fig = px.choropleth(
    df,
    locations="id",
    geojson=district_courts,
    color="numberOfCases",
    color_continuous_scale=px.colors.sequential.Blues,
    hover_name="fidNAME",
    hover_data=["numberOfCases"],
    title="Reverse Payment Cases by District",
    range_color=(0,setRangeMax),
    template="seaborn",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()