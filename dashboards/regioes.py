import pandas as pd
import plotly.express as px
import streamlit as st
import json

from babel.numbers import format_number, format_decimal, format_compact_decimal, format_percent


def right(s, amount):
    return s[-amount:]

def convertMonth(month):
    chunks = month.split('-')

    match chunks[1]:
        case "01":
            return 'Janeiro/' + chunks[0]
        
        case "02":
            return 'Fevereiro/' + chunks[0]
        
        case "03":
            return 'Março/' + chunks[0]
        
        case "04":
            return 'Abril/' + chunks[0]
        
        case "05":
            return 'Maio/' + chunks[0]
        
        case "06":
            return 'Junho/' + chunks[0]
        
        case "07":
            return 'Julho/' + chunks[0]
        
        case "08":
            return 'Agosto/' + chunks[0]
        
        case "09":
            return 'Setembro/' + chunks[0]
        
        case "10":
            return 'Outubro/' + chunks[0]
        
        case "11":
            return 'Novembro/' + chunks[0]
        
        case "12":
            return 'Dezembro/' + chunks[0]
        
# Configurar o layout da página
# st.set_page_config(layout="wide", page_title="Dashboard de Vendas")

# Spinner para mostrar o tempo de aguardar
with st.spinner('Carregando, por favor aguarde...'):

    # Carregar dados geográficos por estado
    geojson = json.load(open('./DATA/brasil-estados.json'))

    # Regiões : Carregar dados de acesso por região
    regions = pd.read_csv('./DATA/db-region-data.csv')
    states = regions.groupby(['State']).agg(
        Quantity = ('OrderID', 'count')
    ).reset_index()

    regions = regions.groupby(['Region']).agg(
        Quantity = ('OrderID', 'count')
    ).reset_index()

    # Adicionar o container
    contHeader = st.container()
    contHeader.title('Vendas por :violet[região e estado]')

    contContent = st.container()

    contCol1, contCol2 = contContent.columns([0.3, 0.7])

    contCol1.subheader('Distribuição por :violet[região]')
    contCol2.subheader('Mapa de calor por :violet[estado]')

    figCom = px.pie(regions, values="Quantity", names="Region")
    contCol1.plotly_chart(figCom, use_container_width=True)

    maxValue = states["Quantity"].max()
    
    figMap = px.choropleth(states, geojson=geojson, locations='State', color='Quantity', range_color=(0, maxValue), color_continuous_scale="Reds", hover_data=['State'], scope='south america')
    figMap.update_layout(
        height=600,
        geo = dict(
            projection = dict(
                type="mercator"
            )
        ),
        margin = dict(
                l=0,
                r=0,
                b=0,
                t=20,
                pad=0,
                autoexpand=True
            ),
    )

    contCol2.plotly_chart(figMap, use_container_width=True)

# Exibir dashboard
st.write()
