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
    page_title='Mapa da Criminalidade SP',
    layout="wide"
)

data_folder = pathlib.Path(__file__).parent.joinpath('data')

# ------------
# - FUNCTIONS
# ------------

# ------------
# - MAIN
# ------------

col1, col2, col3 = st.columns(3)
ano = col1.selectbox('Ano', [y for y in range(2017, 2025)])
if col2.button('Buscar'):
    resp = requests.get(f"https://www.ssp.sp.gov.br/assets/estatistica/transparencia/baseDados/celularesSub/CelularesSubtraidos_{ano}.xlsx", verify=False)
    with open(f'tmp\\CelularesSubtraidos_{ano}.xlsx', 'wb') as output:
        output.write(resp.content)

    df = pd.read_excel(f'tmp\\CelularesSubtraidos_{ano}.xlsx')
    df['HORA_OCORRENCIA'] = df['HORA_OCORRENCIA'].astype('datetime64')
    df.to_parquet(f'data\\CelularesSubtraidos_{ano}.parquet')
    file_to_rem = pathlib.Path(f'tmp\\CelularesSubtraidos_{ano}.xlsx')
    file_to_rem.unlink()
