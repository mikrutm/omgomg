import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import pandas as pd 


st.title('Twitter Tool')
df = st.file_uploader("Upload a CSV")
if df:
    st.dataframe(df)
    st.text(str(df.columns))
    today = date.today()
    st.text(today)

    df['Date'] = pd.to_datetime(df['Date']).dt.date
    end_date = today - timedelta(days = 1)

    start_date = today - timedelta(days =7 )
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)  
    df = df[df.columns[:-1]]
    df = df.loc[mask]
    st.dataframe(df)


    # %%
    #end_date = today

    # Group by name and calculate the sum of numbers
    summary_df = df.groupby('Trend')['Inverted Position'].sum().reset_index()


    # %%
    top=35

    # Rename the columns
    summary_df.columns = ['Trend', 'PopIndex']
    df = summary_df.sort_values(by='PopIndex', ascending=   False).head(top).sort_values(by='PopIndex', ascending=   True)
    df=df.set_index("Trend")
    df["PopIndex"] = df["PopIndex"]/df["PopIndex"].max()
    st.dataframe(df)


