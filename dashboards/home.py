import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

from datetime import datetime
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
        
with st.spinner('Carregando, por favor aguarde...'):
    st.title(":material/cottage: :violet[Bem-vindo!]")
    st.subheader(''' :material/arrow_back: Os seus dashboards estão :violet[prontos]! Use o menu ao lado para iniciar.''')
    st.divider()

    todayYear = datetime.now().strftime('%Y')
    yearBegin = todayYear + '-01'

    containerOverview = st.container()
    containerOverview.header(f"Overview de :violet[{todayYear}]")

    commission = pd.read_csv('./DATA/db-commission-data.csv')
    commission = commission.groupby(["OrderID"]).agg(
        CommissionTotal = ('Commission', 'sum')
    ).reset_index()

    # Vendas : Carregar dados
    sells = pd.read_csv('./DATA/db-sell-data.csv')

    # Vendas : Adicionar informação de comissão
    sells = pd.merge(sells, commission, on="OrderID")

    sells["DateTime"] = pd.to_datetime(sells["DateTime"])
    sells["Date"] = pd.to_datetime(sells["DateTime"]).dt.date
    sells["FinalPrice"] = sells["Price"] - sells["Discount"]
    sells = sells.sort_values("DateTime")

    # Criar uma nova coluna "Month" que contém o ano e o mês para filtrar
    sells["Month"] = sells["DateTime"].apply(lambda x: str(x.year) + "-" + right("0" + str(x.month), 2))

    sells = sells.groupby(['Month']).agg(
        TotalSold = ('FinalPrice', 'sum'),
        TotalCommission = ('CommissionTotal', 'sum')
    ).reset_index()

    sells = sells[sells["Month"] >= yearBegin]

    sells = pd.melt(sells, id_vars=["Month"], value_vars=["TotalSold","TotalCommission"], var_name="Operation", value_name="Amount")
    sells["Operation"] = sells["Operation"].apply(lambda x: "Venda" if x == "TotalSold" else "Comissão")

    figFatYear = px.bar(sells, x="Month", y="Amount", color="Operation", title="Faturamento por mês", barmode="group")
    figFatYear.update_layout(xaxis_title="Mês", yaxis_title="Valor em Reais (R$)")

    containerOverview.plotly_chart(figFatYear, use_container_width=True)

# Exibir o DataFrame filtrado
st.write()
