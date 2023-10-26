from datetime import date, timedelta
import pandas as pd 
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly
import plotly.express as px 

st.title('Twitter Tool')

today = datetime.datetime.now()

end_date = today - timedelta(days = 1)
start_date = today - timedelta(days =7 )
next_year = today.year 
start_date = start_date.date()
end_date = end_date.date()



uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file:
    st.write("filename:", uploaded_file.name)       
    d = st.date_input(
    "Select your vacation for next year",(start_date,end_date),
    format="YYYY.MM.DD",
    )
    start_date = d[0]
    end_date = d[1]
    
    today = date.today()
    st.text(today)
    df=pd.read_csv(uploaded_file)
else:
    df=pd.read_csv("Twitter_trends(11).csv")

 
df['Date'] = pd.to_datetime(df['Date']).dt.date

mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)  
df = df[df.columns[:-1]]
df = df.loc[mask]
    
summary_df = df.groupby('Trend')['Inverted Position'].sum().reset_index()


top = st.slider('Top :', 5, 40,20)


txt = st.text_area(
    "Stop Trends"    )

st.write(f'Pominięte tagi: {list(txt)}')
# Rename the columns
summary_df.columns = ['Trend', 'PopIndex']
df = summary_df.sort_values(by='PopIndex', ascending=   False).head(top).sort_values(by='PopIndex', ascending=   True)
df=df.set_index("Trend")
df["PopIndex"] = df["PopIndex"]/df["PopIndex"].max()
df = df.sort_values(by = ["PopIndex"],ascending=False)

df = df.sort_values(by="PopIndex",ascending=True)
df.loc[~df['column_name'].isin(list(txt))]    

st.dataframe(df)

fig = px.bar(df,x="PopIndex", orientation='h',title=f"Najpopularniejsze hasła na X w okresie {start_date} - {end_date}",width=1000,height=1000) 
st.plotly_chart(fig, theme="streamlit",width=2000,height=2000)
    