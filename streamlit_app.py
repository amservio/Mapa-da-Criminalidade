# ------------
# - IMPORTS
# ------------

import streamlit as st
import pandas as pd
import numpy as np
import math
import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import warnings
import pathlib
import pydeck as pdk

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

# ------------
# - SETUP
# ------------

warnings.filterwarnings('ignore')
st.set_page_config(
    page_title='Template',
    layout="wide"
)

data_folder = pathlib.Path(__file__).parent.joinpath('data')

# ------------
# - FUNCTIONS
# ------------

# ------------
# - MAIN
# ------------

df = pd.DataFrame()
# for item in data_folder.iterdir():
#     if '.csv' in str(item.resolve()):
#         current_df = pd.read_csv(item.resolve(), sep=";")
#         df = pd.concat([df, current_df])

for item in data_folder.iterdir():
    if '.parquet' in str(item.resolve()):
        current_df = pd.read_parquet(item.resolve())
        df = pd.concat([df, current_df])

df['LATITUDE'] = df['LATITUDE'].str.replace('.', '')
df['LATITUDE'] = df['LATITUDE'].str.replace(',', '.')
df['LATITUDE'] = df['LATITUDE'].astype('float64')

df['LONGITUDE'] = df['LONGITUDE'].str.replace('.', '')
df['LONGITUDE'] = df['LONGITUDE'].str.replace(',', '.')
df['LONGITUDE'] = df['LONGITUDE'].astype('float64')


df = df.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'})
df = df[['lat', 'lon', 'MES_ESTATISTICA', 'ANO_ESTATISTICA', 'NATUREZA_APURADA']]
#st.write(len(df.query(f'NATUREZA_APURADA == "FURTO - OUTROS"').query("lat == 0 or lon == 0")))
#st.write(len(df.query(f'NATUREZA_APURADA == "FURTO - OUTROS"').query("lat == 0 or lon == 0"))/len(df))
df = df.query("lat != 0 or lon != 0")



col1, col2, col3 = st.columns(3)
ano = col1.selectbox('Ano', df['ANO_ESTATISTICA'].unique())
natureza = col2.selectbox('Categoria', df['NATUREZA_APURADA'].unique())

st.pydeck_chart(
    pdk.Deck(
        map_style='road',
        tooltip={
                    "html": "<b>Ocorrências:</b> {elevationValue} <br/>",
                    "style": {
                            "backgroundColor": "steelblue",
                            "color": "white"
                    }
                },
        initial_view_state=pdk.ViewState(
            latitude=-23.5489,
            longitude=-46.6388,
            zoom=11,
            pitch=50,
            height=2000
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=df.query(f'NATUREZA_APURADA == "{natureza}" & ANO_ESTATISTICA == {ano}'),
                get_position="[lon, lat]",
                auto_highlight=True,
                radius=100,
                elevation_scale = len(df.query(f'NATUREZA_APURADA == "{natureza}"')),
                elevation_range = [0, 5],
                color_domain=[0, 100],
                color_range=[[0, 255, 0, 60], [100, 155, 0, 60], [255, 255, 0, 60], [155, 100, 0, 60], [255, 0, 0, 60]],
                pickable=True,
                extruded=True,
            ),
        ],
    ), use_container_width=True
)



            # pdk.Layer(
            #     "ScatterplotLayer",
            #     data=df.query('RUBRICA == "Furto (art. 155)"'),
            #     get_position="[lon, lat]",
            #     get_color="[200, 30, 0, 160]",
            #     get_radius=5,
            # ),