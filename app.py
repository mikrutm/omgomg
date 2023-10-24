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


st.text(start_date)
st.text(end_date)

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
 
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)  
    df = df[df.columns[:-1]]
    df = df.loc[mask]
    
    st.text(str(df.columns))
    summary_df = df.groupby('Trend')['Inverted Position'].sum().reset_index()
    top=35
    # Rename the columns
    summary_df.columns = ['Trend', 'PopIndex']
    df = summary_df.sort_values(by='PopIndex', ascending=   False).head(top).sort_values(by='PopIndex', ascending=   True)
    df=df.set_index("Trend")
    df["PopIndex"] = df["PopIndex"]/df["PopIndex"].max()
    df = df.sort_values(by = ["PopIndex"],ascending=False)
    st.dataframe(df)
    
    import matplotlib.pyplot as plt
    import numpy as np

    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    st.pyplot(fig)

