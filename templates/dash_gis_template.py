
# Standard library imports
from typing import List, Dict, Union, Optional, Tuple, Iterable, Any

# Third party library imports
import dash
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import plotly.express as px
import pandas as pd
from plotly.missing_ipywidgets import FigureWidget


#######################
# Data initialization #
#######################

# assume you have a "long-form" data frame
location_df = pd.DataFrame({
    "Lat": [34.0536, 33.5724, 31.2242, 12.8029, 40.7127],
    "Lon": [-118.2427, -7.6570, 29.8848, 14.8877, -74.0059],
    "Amount": [7, 1, 6, 3, 2],
    "City": ["Los Angeles", "Casablanca", "Alexandria", "Chad", "New York"],
})


#################
# UI Components #
#################

# Initialize UI Card for filtering
controls = dbc.Card([
    html.H2("Control Panel:"),
    dbc.FormGroup([
        dbc.Label("Origin Location"),
        dcc.Dropdown(
            id="location-origin",
            options=[{"label": col, "value": col} for col in location_df["City"].unique()],
        ),
    ]),
    dbc.FormGroup([
        dbc.Label("Destination Location"),
        dcc.Dropdown(
            id="location-destination",
            options=[{"label": col, "value": col} for col in location_df["City"].unique()],
        ),
    ]),
    dbc.FormGroup([
        dbc.Label("Inbetween Stops"),
        dcc.Dropdown(
            id="location-between",
            options=[{"label": col, "value": col} for col in location_df["City"].unique()],
            multi=True,
        ),
    ]),
], body=True)

# Initializing and organizing application layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1('Dash GIS Example App'),
    html.Hr(),
    dbc.Row([
        dbc.Col(controls, md=4),
        dbc.Col(dcc.Graph(id="example-gis-graph"), md=8),
    ], align="center"),
], fluid=True)


######################
# Callback Functions #
######################

@app.callback(
    Output("example-gis-graph", "figure"),
    [Input("location-origin", "value"), Input("location-destination", "value"), Input("location-between", "value")],
)
def make_map(origin: Optional[str], destination: Optional[str], steps: Optional[List[str]]) -> FigureWidget:
    """Generate map for basic GIS dash app

    Parameters
    ----------
    origin: str or None
        name of origin city
    destination: str or None
        name of destination city
    steps: List[str] or None:
        list of cities along the route

    Returns
    ----------

    fig: plotly figure
        geographic line plot representing data
    """
    # Filtering data set based on filter inputs
    selected_locations = []
    if origin is not None:
        selected_locations.append(origin)
    if steps is not None and origin is not None and destination is not None:
        selected_locations.extend(steps)
    if destination is not None:
        selected_locations.append(destination)
    if len(selected_locations) == 0:
        return px.line_geo(data_frame=location_df.head(1), lat="Lat", lon="Lon")

    selected_df = pd.DataFrame({"City": selected_locations})
    selected_df = selected_df.assign(OrderId=selected_df.index + 1)

    map_data = location_df[location_df["City"].isin(selected_locations)].reset_index(drop=True)
    if steps is not None and len(steps) > 0:
        map_data = pd.concat([map_data, location_df[location_df["City"].isin(steps)]], ignore_index=True). \
            join(selected_df.set_index("City"), on="City"). \
            sort_values("OrderId").drop(["OrderId"], axis=1)
        map_data = map_data.assign(Group=[x for x in range(1, len(selected_locations)) for _ in range(2)])
    else:
        map_data = map_data.assign(Group=1)

    # Generate map based on filtered data
    fig = px.line_geo(
        data_frame=map_data,
        lat="Lat",
        lon="Lon",
        hover_name="City",
        line_group="Group",
        color="Group",
        line_dash="Group",
    )

    return fig


@app.callback(
    [Output("location-origin", "options"), Output("location-destination", "options")],
    [Input("location-origin", "value"), Input("location-destination", "value"), Input("location-between", "value")]
)
def disable_single_location_options(origin: str, destination: str, between: Union[List[None],str]) -> Tuple[List[Dict[str,str]], List[Dict[str,str]]]:
    all_locs = location_df["City"].unique()
    between = [] if between is None else between
    origin_between = [origin, *between]
    dest_between = [destination, *between]

    origin_options = [{"label": col, "value": col, "disabled": col in dest_between} for col in all_locs]
    dest_options = [{"label": col, "value": col, "disabled": col in origin_between} for col in all_locs]

    return origin_options, dest_options


@app.callback(
    Output("location-between", "options"),
    [Input("location-origin", "value"), Input("location-destination", "value")]
)
def remove_between_location_options(origin: str, destination: str) -> List[Dict[str,Union[str,bool]]]:
    """Remove options that have already been selected"""
    locations = [origin, destination]
    if any([location is None for location in locations]):
        locations = list(location_df["City"].unique())
    return [{"label": col, "value": col, "disabled": col in locations} for col in location_df["City"].unique()]


if __name__ == "__main__":
    app.run_server(debug=True)
