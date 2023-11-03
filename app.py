from datetime import date, timedelta
import pandas as pd 
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly
import plotly.express as px 

base="light"

st.title('Twitter Tool')
tab1, tab2 = st.tabs(["Top", "Trend"])

with st.sidebar:

   
    today = datetime.datetime.now()
    end_date = today - timedelta(days = 1)
    start_date = today - timedelta(days =7 )
    next_year = today.year 
    start_date = start_date.date()
    end_date = end_date.date()



    uploaded_file = st.file_uploader("Wgraj Trend CSV z maila")
    if uploaded_file:
        st.write("filename:", uploaded_file.name)       
        d = st.date_input(
        "Wybierz zakres do analizy",(start_date,end_date),
        format="YYYY.MM.DD",
        )
        start_date = d[0]
        end_date = d[1]

        df=pd.read_csv(uploaded_file)
    else:
        df=pd.read_csv("Twitter_trends(14).csv")
        d = st.date_input(
        "Wybierz zakres do analizy",(start_date,end_date),
        format="YYYY.MM.DD",
        )
        start_date = d[0]
        end_date = d[1]
    
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)  
    df = df[df.columns[:-1]]
    df = df.loc[mask]

    summary_df = df.groupby('Trend')['Inverted Position'].sum().reset_index()


    
with tab1:
    st.subheader('Top trends Twitter')
    top = st.slider('Ile najpopularniejszych tagów :', 5, 40,20)


    txt = st.text_area(
        "Stop Trends (wpisz trendy do ponięcie w formacie : Trend1,Trend2,...)"    )

    txt = txt.split(sep=",")
    st.write(f'Pominięte tagi: {txt}')
    # Rename the columns
    summary_df.columns = ['Trend', 'PopIndex']
    df_s = summary_df.sort_values(by='PopIndex', ascending=   False).head(top).sort_values(by='PopIndex', ascending=   True)
    df_s=df_s.set_index("Trend")
    df_s["PopIndex"] = df_s["PopIndex"]/df_s["PopIndex"].max()
    df_s = df_s.sort_values(by = ["PopIndex"],ascending=True)

    df_s = df_s.sort_values(by="PopIndex",ascending=True)

    mask = ~df_s.index.isin(txt)
    df_s=df_s[mask]
    st.dataframe(df_s)

    fig = px.bar(df_s,x="PopIndex", orientation='h',title=f"Najpopularniejsze hasła na X w okresie {start_date} - {end_date}",width=1000,height=800, labels=
                 {"PopIndex":"Wskaźnik Popularności"
                 },template="simple_white") 
    st.plotly_chart(fig, theme="streamlit",width=1000,height=800)
with tab2:
    st.subheader('Trend')
