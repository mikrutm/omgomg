from datetime import date, timedelta
import pandas as pd 
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly
import plotly.express as px 

base="light"


tab1, tab2 = st.tabs(["Top", "Trend"])

def generate_updated_dataframe(start_date, end_date, df2):
    date_range = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d')
    data = {'Date': date_range}
    df = pd.DataFrame(data)
    merged_df = df.merge(df2, on='Date', how='left')
    merged_df['Inverted Position'] = merged_df['Inverted Position'].fillna(0)
    merged_df = merged_df.drop('Inverted Position', axis=1)
    return merged_df

with st.sidebar:
    st.title('Twitter Tool')
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
    txt1 = st.text_area(
        "Wybierz pierwszą grupę tagów : "    )

    txt1 = txt1.split(sep=",")
    st.write(f'Tagi pierwszej grupy : {txt1}')
    txt2 = st.text_area(
        "Wybierz druga grupę tagów : "    )

    txt2 = txt2.split(sep=",")
    st.write(f'Tagi drugiej grupy : {txt2}')

    df_g = df[df['Trend'].isin(txt1)]

    df_g = df_g['Inverted Position'].groupby(df_g['Date']).sum()
    df_g= generate_updated_dataframe(start_date,end_date,df_g)
    
    fig_1 = px.bar(df_g,title=f"Popularność grupy tagów {txt1} w okresie {start_date} - {end_date}",template="simple_white") 
    fig_1.update_layout(yaxis_range=[start_date,end_date])
    st.plotly_chart(fig_1, theme="streamlit")

    df_g2 = df[df['Trend'].isin(txt2)]

    df_g2 = df_g2['Inverted Position'].groupby(df_g2['Date']).sum()
    df_g2= generate_updated_dataframe(start_date,end_date,df_g2)
    fig_2 = px.bar(df_g2,title=f"Popularność grupy tagów {txt2} w okresie {start_date} - {end_date}",template="simple_white") 
    st.plotly_chart(fig_2, theme="streamlit")

