import pandas as pd
import streamlit as st
import json
import warnings

#df = pd.read_excel('tmp\\CelularesSubtraidos_2017.xlsx')
#df.to_csv('tmp\\CelularesSubtraidos_2017.csv', index=False)

warnings.filterwarnings('ignore')
st.set_page_config(
    page_title='Mapa da Criminalidade SP',
    layout="wide"
)

ano = 2017

@st.cache_data
def get_csv():
    df = pd.read_csv(f'tmp\\CelularesSubtraidos_{ano}.csv')
    return df

df = get_csv().head(500)
st.dataframe(df.columns, use_container_width=True)

collection = {
    'type': 'FeatureCollection',
    'features': []
}
for idx, row in df.iterrows():
    if not pd.isna(row['LATITUDE']) and (row['LATITUDE'] != 0 or row['LONGITUDE'] != 0):
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['LONGITUDE'], row['LATITUDE']]
            },
            'properties': {
                'categoria': row['RUBRICA']
            }
        }
        collection['features'].append(feature)

with open(f'geojson\CelularesSubtraidos_{ano}.geojson', 'w') as fp:
    json.dump(collection, fp)