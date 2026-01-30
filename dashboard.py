import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Configuração da Página
st.set_page_config(page_title="Dashboard - Karaberu", layout="wide")

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Busca dados
response = supabase.table("projects").select("*").neq("status", "descartado").execute()
df = pd.DataFrame(response.data)

st.title("Dashboard de Projetos - Karaberu")
st.markdown("---") 

if not df.empty:
    # Tratamento de dados
    df['price'] = pd.to_numeric(df['price']).fillna(0)
    df['cost'] = pd.to_numeric(df['cost']).fillna(0)
    df['profit'] = df['price'] - df['cost']
    
    # Metricas principais
    total_vendas = df[df['status'] == 'vendido']['price'].sum()
    total_lucro = df['profit'].sum()

    m_col1, m_col2, m_col3 = st.columns(3) 
    m_col1.metric("Total Vendido", f"R$ {total_vendas:,.2f}")
    m_col2.metric("Lucro Total", f"R$ {total_lucro:,.2f}")
    m_col3.metric("Projetos Ativos", len(df))

    st.markdown("---")

    # Linha de Gráficos
    chart_col1, chart_col2 = st.columns([1, 1.2]) 

    with chart_col1:
        df_status = df['status'].value_counts().reset_index()
        df_status.columns = ['status', 'quantidade']

        fig_status = px.pie(
            df_status, 
            values='quantidade', 
            names='status', 
            title='Distribuição de Status',
            hole=0.4,
            height=400
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with chart_col2:
        fig_comp = px.bar(
            df, 
            x='name', 
            y=['price', 'cost'], 
            title='Preço vs Custo por Projeto',
            labels={'value': 'Reais (R$)', 'variable': 'Tipo', 'name': 'Projetos'},
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_comp, use_container_width=True)

else:
    st.warning("Nenhum dado encontrado.")