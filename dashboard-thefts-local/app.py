########################################################################################################################
############################################## MODULOS PARA EL DASHBOARD ###############################################
########################################################################################################################

# -*- coding: utf-8 -*-

#Modulos para gestionar dataframes, cálculos con vectores y matrices
import numpy  as np
import pandas as pd

#Modulos de visualización
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import geopandas

#Modulos del Dash para generar el dashboard
from dash import Dash, dcc, html, Input, Output, State
from flask import Flask
server = Flask(__name__)

#Tema de los gráficos
sns.set_theme()
sns.set_context("paper")

######################## Importando funciones creadas para el funcionamiento del DashBoard ###############

#importing model functions
import model_fn as md

# dropdown_values
import dropdown_values as dpv 

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

#app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/",
#                external_stylesheets=external_stylesheets)
#
#app2 = dash.Dash(__name__, server=server, routes_pathname_prefix="/model/",
#                external_stylesheets=external_stylesheets)

#Local server
app = Dash(__name__, server=server, routes_pathname_prefix="/dash/",
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

#Servidor remoto
#server = app.server
#app.scripts.config.serve_locally = False

#######################################################################################################################
#########################################  Configuración inicial del mapa ################################################
#######################################################################################################################

#Graph config
config_graph = {"displayModeBar": True,
              "scrollZoom": False,
              "autosizable":True,
              "showAxisDragHandles":False}

#Reading GeoJSON
barrios_geopandas = geopandas.read_file("./assets/barrios.geojson", driver="GeoJSON")
barrios_geopandas["geometry"] = barrios_geopandas["geometry"].to_crs("EPSG:4326")

#First Map
fig = px.choropleth_mapbox(barrios_geopandas,
                            locations="GEOID",
                            geojson=barrios_geopandas,
                            hover_name="Barrio",
                            #featureidkey="GEOID",
                            zoom=11,
                            mapbox_style="carto-positron",
                            center={"lat": 10.97, "lon": -74.8},
                            color_continuous_scale="YlOrBr",
                            opacity=0.5,
                            )
fig.update_layout(title="", paper_bgcolor="#F8F9F9",
                   margin={"r": 0, "t": 0, "l": 0, "b": 0})


######################################################################################################################
#############################################   Dashboard Layout  ####################################################
######################################################################################################################

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        #First row (Image and Title)
        html.Div(
            [
                #Image Uninorte
                html.Div(
                    [
                        html.Div([
                        html.Img(
                            src=app.get_asset_url("1200px-Logo_uninorte_colombia.jpg"),
                            id="plotly-image",
                            style={
                                "height": "80px",
                                "width": "auto",
                                "margin-bottom": "10px",
                            },
                        ),
                        ])
                    ],
                    className="one column",
                ),
                #Container for Title
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Modelamiento geo-espacial y temporal del robo en el área metropolitana de Barranquilla",
                                    style={"margin-bottom": "0px"},
                                ),

                            ]
                        )
                    ],
                    className="eleven columns",
                    id="title",
                ),

            ],
            id="header",
            className="row flex-display",
        ),
       #Second container (filter, KPIs, scatter and histogram)
        html.Div(
            [
                #Column Filter
                html.Div(
                    [
                        html.P(
                            "Por favor complete las variables:",
                            className="control_label",
                        ),
                        html.Br(),
                        #html.P(
                        #    "Categoría de sitio: ",
                        #    className="control_label"
                        #    ),
                        #dcc.Dropdown(
                        #    id="cat_model",
                        #    options=dpv.CATEGORIA_SITIO,
                        #    multi=False,
                        #    value="Categoria de sitio_AEROPUERTO",
                        #    className="dcc_control",
                        #),
                        #html.P(
                        #    "Arma empleada:",
                        #    className="control_label",
                        #),
                        #dcc.Dropdown(
                        #    id="arma_model",
                        #    options=dpv.ARMA_EMPLEADA,
                        #    multi=False,
                        #    value="Arma empleada_ESCOPOLAMINA",
                        #    className="dcc_control",
                        #),
                        #html.P(
                        #    "Mes del año:",
                        #    className="control_label",
                        #),
                        #dcc.Dropdown(
                        #    id="mes_model",
                        #    options=[
                        #        {"label": "Enero", "value":"Month_1"},
                        #        {"label": "Febrero", "value":"Month_2"},
                        #        {"label": "Marzo", "value":"Month_3"},
                        #        {"label": "Abril", "value":"Month_4"},
                        #        {"label": "Mayo", "value":"Month_5"},
                        #        {"label": "Junio", "value":"Month_6"},
                        #        {"label": "Julio", "value":"Month_7"},
                        #        {"label": "Agosto", "value":"Month_8"},
                        #        {"label": "Septiembre", "value":"Month_9"},
                        #        {"label": "Octubre", "value":"Month_10"},
                        #        {"label": "Noviembre", "value":"Month_11"},
                        #        {"label": "Diciembre", "value":"Month_12"}
                        #    ],
                        #    multi=False,
                        #    value="Month_1",
                        #    className="dcc_control",
                        #),
                        html.P(
                            "Día de la semana:",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="day_model",
                            options=[
                                {"label": "Lunes", "value":"WeekDay_0"},
                                {"label": "Martes", "value":"WeekDay_1"},
                                {"label": "Miércoles", "value":"WeekDay_2"},
                                {"label": "Jueves", "value":"WeekDay_3"},
                                {"label": "Viernes", "value":"WeekDay_4"},
                                {"label": "Sábado", "value":"WeekDay_5"},
                                {"label": "Domingo", "value":"WeekDay_6"}
                            ],
                            multi=False,
                            value="WeekDay_0",
                            className="dcc_control",
                        ),
                        #html.Br(),
                        #html.Br(),
                        html.P(
                            "Tiempo:",
                            className="control_label",
                        ),                        
                        dcc.RadioItems(
                            id="time_model",
                            options=[
                                {"label": "Madrugada (12AM - 6AM)", "value": "Timeframe_Madrugada"},
                                {"label": "Día (7AM - 5PM)", "value": "Timeframe_Dia"},
                                {"label": "Noche (6PM - 11PM)", "value": "Timeframe_Noche"}
                            ],
                            value="Timeframe_Madrugada",
                            #labelStyle={"display": "inline-block"}
                        ),
                        #html.Br(),
                        #html.P(
                        #    "Días especiales",
                        #    className="control_label",
                        #),
                        #dcc.Checklist(
                        #    id="special_days",
                        #    options=[
                        #        {"label": "Quincena", "value": "Quincena"},
                        #        {"label": "Día de la madre", "value": "Dia_Madre"},
                        #        {"label": "Carnaval", "value": "Carnaval"}
                        #        ],
                        #    value=["Quincena"],
                        #    labelStyle={"display": "inline-block"}
                        #),
                        #html.Br(),
                        html.Br(),
                        html.Button(id="submit-button-state",
                                        n_clicks=0, children="Submit"),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),  
                    ],
                    className="pretty_container two columns",
                    id="cross-filter-options",
                ),
                #Container for KPIs
                html.Div(
                    [
                        dcc.Graph(
                                id="Model_map", figure=fig, config = config_graph),
                    ],
                    id="right-column2",
                    className="pretty_container ten columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

## Create callbacks
@app.callback(
    [     
        Output("Model_map", "figure"),
    ],
    [
        Input("submit-button-state", "n_clicks")
    ],
    [
        #State(component_id="cat_model", component_property="value"),
        #State(component_id="arma_model", component_property="value"),
        #State(component_id="mes_model", component_property="value"),
        State(component_id="day_model", component_property="value"),
        State(component_id="time_model", component_property="value"),
        #State(component_id="special_days", component_property="value"),
    ],
)
def update_map(n_clicks, day_model, time_model, ):

    if ((n_clicks==0) or (day_model == None) or (time_model == None)):
            mapa = fig
    else:
        mapa = md.poisson_prediction(barrios_geopandas, day_model, time_model)
    return [go.Figure(data=mapa)]

# Main
#if __name__ == "__main__":
#    app.run_server(debug=True)

#Main
if __name__ == "__main__":
    app.run_server(debug=True, port=80, host="0.0.0.0")
