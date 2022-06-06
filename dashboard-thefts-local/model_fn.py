#Modulos nativos de Python
import warnings

#Modulos para gestionar dataframes, cálculos con vectores y matrices
import numpy  as np
import pandas as pd
import plotly.express as px

#Modulos para la generación de modelos
import pickle
from sklearn.linear_model import PoissonRegressor

#importando variables necesarias
import dropdown_values as dpv

warnings.filterwarnings("ignore")

#Función que estima las cantidades de robo en base al modelo
def poisson_prediction(bar_geo, day_model, time_model):

    #Leyendo el modelo de Poisson ya entrenado
    model_poisson = pickle.load(open("./assets/poisson_model.pickle", "rb"))

    #Creando el dataframe que se usará para calcular las predicciones
    df_pred = pd.DataFrame(np.diag([1] * len(dpv.BARRIOS)), columns=dpv.BARRIOS)

    #Creando el diccionario de valores escogidos por el usuario en el dashboard
    v = 1
    upd_dict = {k:v for k in [day_model, time_model]}

    #for x in special_days:
    #    upd_dict[x] = 1

    #Valores usados para la predicción en cada barrio
    pr_col = dpv.PREDICT_COLUMNS.copy()
    pr_col.update(upd_dict)

    #Actualizando el dataframe
    df_pred[list(pr_col.keys())] = list(pr_col.values())

    # Constructing dataframe to map neighborhood to predicted value
    df_predict_values = pd.DataFrame(columns=["Barrio", "Cantidad"])

    #Haciendo las predicciones
    df_predict_values["Barrio"] = [x.split("_")[-1] for x in dpv.BARRIOS]
    df_predict_values["Cantidad"] = model_poisson.predict(df_pred)

    #Haciendo el merge con barrios_geopandas
    bar_geo2 = bar_geo[["Barrio", "GEOID"]].merge(df_predict_values, on="Barrio", how="left")
    bar_geo2["Cantidad"] = bar_geo2["Cantidad"].fillna(0)

    mapa = px.choropleth_mapbox(bar_geo2,
                                locations="GEOID",
                                color="Cantidad",
                                geojson=bar_geo,
                                hover_name="Barrio",
                                #featureidkey="Cantidad",
                                zoom=11,
                                mapbox_style="carto-positron",
                                center={"lat": 10.97, "lon": -74.8},
                                color_continuous_scale="YlOrBr",
                                range_color=(0,12),
                                opacity=0.5,
                                labels={"Cantidad": "Cantidad de robos predicha:"}
                                )
    mapa.update_layout(title='', paper_bgcolor="#F8F9F9",
                       margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return mapa
