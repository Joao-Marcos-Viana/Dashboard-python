import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from supabase import create_client, Client
from dotenv import load_dotenv
import os
#---

load_dotenv()

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

response = supabase.table("projects").select("*").neq("status", "descartado").execute()
df = pd.DataFrame(response.data)
#---

if not df.empty:
    
    df['price'] = pd.to_numeric(df['price']).fillna(0)
    df['cost'] = pd.to_numeric(df['cost']).fillna(0)
    
    df['profit'] = df['price'] - df['cost']
    
    total_vendas = df[df['status'] == 'vendido']['price'].sum()
    total_lucro = df['profit'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Vendido", f"R$ {total_vendas:,.2f}")
    col2.metric("Lucro Total", f"R$ {total_lucro:,.2f}")

    df_status = df['status'].value_counts().reset_index()
    df_status.columns = ['status', 'quantidade']

    fig_status = px.pie(
        df_status, 
        values='quantidade', 
        names='status', 
        title='Distribuição de Status dos Projetos',
        hole=0.4
    )
    st.plotly_chart(fig_status)

    fig_comp = px.bar(
        df, 
        x='name', 
        y=['price', 'cost'], 
        title='Preço vs Custo por Projeto',
        barmode='group' 
    )
    st.plotly_chart(fig_comp)