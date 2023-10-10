import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.font_manager import FontProperties
from datetime import date, timedelta
import pandas as pd 


st.title('Twitter Tool')
df = st.file_uploader("Upload a CSV")



font = FontProperties()
plt.style.use('bmh')
font.set_name('Lato')
csv_filename = 'Twitter_trends(9).csv'
df= pd.read_csv(csv_filename)

#092D64
plt.rcParams.update({'text.color' : "#092D64",
                     'axes.labelcolor' : "#092D64"})

today = date.today()

params = {'legend.fontsize': 30,
          'legend.handlelength': 2}

plt.rcParams.update(params)
df['Date'] = pd.to_datetime(df['Date']).dt.date
end_date = today - timedelta(days = 1)

start_date = today - timedelta(days =7 )
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)  
df = df[df.columns[:-1]]
df = df.loc[mask]
print(df)


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
print(df)
fig, ax = plt.subplots(figsize=(30, 21), dpi=72)
ax.set_facecolor('#F6F6F6')
plt.rcParams['savefig.facecolor']='#F6F6F6'

plt.rcParams.update(params)
for label in ( ax.get_yticklabels()):
	label.set_fontsize(50)
for label in ( ax.get_xticklabels()):
	label.set_fontsize(42)
ax.ticklabel_format( axis='x', style='plain')

df["PopIndex"].plot(kind='barh',ax=ax)
plt.xlabel("Wskaźnik popularności", fontsize= 60)
plt.ylabel("Hasła", fontsize= 70)
plt.subplots_adjust(bottom=0.85)
ax.tick_params(axis='x', colors= "#092D64")
ax.tick_params(axis='y', colors="#092D64")
fig.tight_layout()
#plt.title("Najpopularniejsze hasła wyszukiwane w Google", fontsize= 30)
plt.savefig(f"trends{start_date}-{end_date}_top{top}.svg", format = "svg",dpi=600,transparent = True)
#plt.show()

print(start_date)
print(end_date)



