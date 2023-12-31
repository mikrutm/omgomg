from datetime import date, timedelta
import pandas as pd 
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly
import plotly.express as px 

base="light"
def add_datetime_column(df):
    def add_time_column(df):
        times = []
        hour = 0
        interval = 50
        for i in range(len(df)):
            times.append(f"{str(hour).zfill(2)}:00")
            if (i + 1) % interval == 0:
                if hour == 0:
                    hour = 23
                else:
                    hour = (hour - 1) % 24
        df['Time'] = times
        return df

    df_with_time_column = add_time_column(df)

    # Połączenie kolumn 'Date' i 'Time' w nową kolumnę 'DateTime' w formacie daty i czasu
    df_with_time_column['DateTime'] = pd.to_datetime(df_with_time_column['Date'].astype(str) + ' ' + df_with_time_column['Time'])

    return df_with_time_column


tab1, tab2, tab3 = st.tabs(["Top", "Trend","Alert"])

def generate_updated_dataframe(start_date, end_date, df2):
    
    df2 = df2.reset_index()
    df2.columns = ['Date', 'Inverted Position']
    
    date_range = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d')
    data = {'Date': date_range, 'Inverted Position': [0] * len(date_range)}
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])
    merged_df = df.merge(df2, on='Date', how='left')
    
    merged_df['Inverted Position'] = merged_df['Inverted Position_y'].fillna(0)
    merged_df = merged_df.drop(['Inverted Position_x', 'Inverted Position_y'], axis=1)
    
    return merged_df

with st.sidebar:
    st.title('Twitter Tool')
    today = datetime.datetime.now()
    end_date = today - timedelta(days = 0)
    start_date = today - timedelta(days =1 )
    next_year = today.year 
    start_date = start_date.date()
    end_date = end_date.date()

    h=st.number_input("Wysokość wykresu", value=600,step =25)
    w=st.number_input("Szerokość wykresu", value=700,step =25)
    f=st.number_input("Wielkość fontu", 15)

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
        df_time = add_datetime_column(df)
    
    else:
        df=pd.read_csv("Twitter_trends(14).csv")
        df_time = add_datetime_column(df)
 
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

    fig = px.bar(df_s,x="PopIndex", orientation='h',title=f"Najpopularniejsze hasła na X w okresie {start_date} - {end_date}",width=w,height=h, labels=
                 {"PopIndex":"Wskaźnik Popularności",
                 },template="simple_white") 
    fig.update_yaxes(tickfont=dict(family="Lato",
                                 size=f,color="#092D64"))
    fig.update_xaxes(tickfont=dict(family="Lato",color="#092D64"))
    
    fig.update_layout(
    font_family="Lato",
    font_color="#092D64",
    title_font_family="Lato",
    title_font_color="#092D64")
    

    st.plotly_chart(fig, theme="streamlit",width=w,height=h,size = f)
    st.text('Wykres przedstawia hasła charakterystyczne dla najważniejszych tematów na portalu X \n w badanym okresie. Miarą wagi poszczególnych haseł jest wskaźnik popularności, \n który jest obliczany na podstawie częstości występowania hasła i jego pozycji w \n zestawieniach cząstkowych. Wartość wskaźnika dla poszczególnych haseł jest \n normalizowana do jedynki względem wartości maksymalnej z danego okresu.')

with tab2:

    st.subheader('Trend')
    txt1 = st.text_area(
        "Wybierz pierwszą grupę tagów : "    )

    txt1 = txt1.split(sep=",")
    st.write(f'Tagi pierwszej grupy : {txt1}')
   

    df_g = df[df['Trend'].isin(txt1)]

    df_g = df_g['Inverted Position'].groupby(df_g['Date']).sum()
    df_g= generate_updated_dataframe(start_date,end_date,df_g)

    fig_1 = px.bar(df_g,x = "Date",y="Inverted Position",title=f"Popularność grupy tagów {txt1} w okresie {start_date} - {end_date}",template="simple_white") 
    st.plotly_chart(fig_1, theme="streamlit")    
    
    txt2 = st.text_area(
        "Wybierz druga grupę tagów : "    )

    txt2 = txt2.split(sep=",")
    st.write(f'Tagi drugiej grupy : {txt2}')

    df_g2 = df[df['Trend'].isin(txt2)]

    df_g2 = df_g2['Inverted Position'].groupby(df_g2['Date']).sum()
    df_g2= generate_updated_dataframe(start_date,end_date,df_g2)
    
    fig_2 = px.bar(df_g2,x = "Date",y="Inverted Position",title=f"Popularność grupy tagów {txt2} w okresie {start_date} - {end_date}",template="simple_white") 
    st.plotly_chart(fig_2, theme="streamlit")
    merged_df = df_g2.merge(df_g, on='Date', suffixes=('_2', '_1'))

    print(merged_df)
    trend1 = st.text_input("Nazwa grupy pierwszej",value= "Grupa1")
    trend2 = st.text_input("Nazwa grupy drugiej",value= "Grupa2")
    #merged_df.rename({'Inverted Position_1': trend1, "Inverted Position_2":trend2}, axis='columns',inplace=True)

    fig_3 = px.bar(merged_df,x = "Date",y = ["Inverted Position_1","Inverted Position_2"],title=f"Popularność grup tagów w okresie {start_date} - {end_date}",template="simple_white",labels={'Date': 'Data', 'value':'Wskaźnik Popularności'}) 
 
    newnames = {'Inverted Position_1':trend1, 'Inverted Position_2': trend2}

    fig_3.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
    st.plotly_chart(fig_3, theme="streamlit")
with tab3:


    
    st.subheader('Rozkład godzinowy zainteresowania')

    txt3 = st.text_area(
        "Trend Godzinowy : "    )

    #txt3 = txt3.split(sep=",")
    st.write(f'Obserwujesz godzinowo tag: {txt3}')
    #df_time[["Inverted Position","Trend","DateTime"]]
    selected_rows = df_time[df_time['Trend'] == str(txt3)]
    
    fig_4 = px.bar(selected_rows,x = "DateTime",y = "Inverted Position",title=f"Godzinowy Trend") 
    st.plotly_chart(fig_4, theme="streamlit")
