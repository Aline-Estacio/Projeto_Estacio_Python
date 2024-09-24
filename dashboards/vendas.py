import pandas as pd
import plotly.express as px
import streamlit as st

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
    # Comissão : Carregar dados e sumarizar
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

    # Gerar vendas, descontos e comissão agregadas
    sumSells = sells.groupby(['Month', 'Date']).agg(
        PriceTotal = ('Price', 'sum'),
        DiscountTotal = ('Discount', 'sum'),
        TotalSold = ('FinalPrice', 'sum'),
        TotalCommission = ('CommissionTotal', 'sum')
    ).reset_index()

    # Adicionar filtro de mês na lateral do dashboard
    filteredMonths = (sells.sort_values("Month", ascending=[False]))["Month"].unique()
    month = st.sidebar.selectbox("Selecione o Mês", filteredMonths, format_func=lambda x: convertMonth(x))

    # Adicionar o container
    contHeader = st.container()
    contHeader.title("Dashboard de Vendas")

    # Comissão
    # DataFrame para gerar gráfico de barra mostrando total vendido versus comissão
    sellsAndCommission = pd.melt((sumSells[sumSells["Month"] == month]), id_vars=["Month"], value_vars=["TotalSold","TotalCommission"], var_name="Operation", value_name="Amount")
    sellsAndCommission["Operation"] = sellsAndCommission["Operation"].apply(lambda x: "Venda" if x == "TotalSold" else "Comissão")

    # Total Vendido
    totalSoldAmount = round((sumSells[sumSells["Month"] == month])["TotalSold"].sum(), 2)
    totalSoldAmount = format_decimal(totalSoldAmount, locale='pt_BR')

    totalCommission = round((sumSells[sumSells["Month"] == month])["TotalCommission"].sum(), 2)
    totalCommission = format_decimal(totalCommission, locale='pt_BR')

    contHeader.header("Total vendido por dia em :violet[" + convertMonth(month) + "]")
    # contHeader.markdown("Total Vendido R$" + " :blue[" + str(totalSoldAmount) + "] | Total de Comissão R$" + " :blue[" + str(totalCommission) + "]")
    contHeader.markdown(f'''Total Vendido :violet[R$ {str(totalSoldAmount)}] | Total de Comissão :violet[R$ {str(totalCommission)}]''')

    st.divider()

    contTotalFat = st.container()

    fatCol1, fatCol2 = contTotalFat.columns([0.7, 0.3])

    fatCol1.subheader('Distribuição por :violet[dia]')
    fatCol2.subheader('Taxa de :violet[comissão] sobre vendas')

    # cont.subheader("Total de comissão em :blue[" + convertMonth(month) + "] : R$ " + str(totalCommission))

    # col1, col2 = st.columns([1]) # Primeira linha com duas colunas

    # Criar o gráfico de faturamento por dia
    figFatDay = px.bar((sumSells[sumSells["Month"] == month]), x="Date", y="TotalSold")
    figFatDay.update_layout(xaxis_type='category', xaxis_title="Dia", yaxis_title="R$ Vendido")
    figFatDay.update_xaxes(tickangle=45)

    # Exibir o gráfico na primeira coluna
    fatCol1.plotly_chart(figFatDay, use_container_width=True)

    # Criar gráfico de pizza para distribuição da comissão
    figCom = px.pie(sellsAndCommission, values="Amount", names="Operation")
    fatCol2.plotly_chart(figCom, use_container_width=True)


# Exibir dashboard
st.write()
