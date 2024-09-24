import streamlit as st

home_page = st.Page("./dashboards/home.py", title="Página Inicial", icon=":material/cottage:")
vendas_page = st.Page("./dashboards/vendas.py", title="Total de Vendas", icon=":material/price_check:")
regioes_page = st.Page("./dashboards/regioes.py", title="Vendas por Região", icon=":material/price_check:")

pg = st.navigation([home_page, vendas_page, regioes_page])
st.set_page_config(layout="wide")
pg.run()