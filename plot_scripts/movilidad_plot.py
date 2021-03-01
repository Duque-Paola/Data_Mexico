import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns

URL="https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
#df=pd.read_csv(URL, low_memory=False) 
df=pd.read_csv(URL, low_memory=False)


df=df[df.country_region_code=='MX']
df['date'] =  pd.to_datetime(df['date'])
df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
df.head()

df.shape

df.info()

df.isnull().sum()

df.drop('sub_region_2',1,inplace=True)

null_columns=df.columns[df.isnull().any()]
print(df[df.isnull().any(axis=1)][null_columns].head(63)) #The null values

list(df)
df.rename(columns={'sub_region_1': 'Province',
                   'retail_and_recreation_percent_change_from_baseline': 'Retail_and_Recreation', 
                   'grocery_and_pharmacy_percent_change_from_baseline':'Grocery_and_Pharmacy', 
                   'parks_percent_change_from_baseline':'Parks',
                   'transit_stations_percent_change_from_baseline': 'Transit_Stations',
                   'workplaces_percent_change_from_baseline':'Workplaces',
                   'residential_percent_change_from_baseline': 'Residences',
                   'date':'Date'},inplace=True)
df=df[['Date',
       'Province',
 'Retail_and_Recreation',
 'Grocery_and_Pharmacy',
 'Parks',
 'Transit_Stations',
 'Workplaces',
 'Residences']]


#############################################################################

df_Jal = df[df.Province == 'Jalisco']
df_Jal_W = df_Jal.resample("W").sum()
fig,ax = plt.subplots()
ax.plot(df_Jal_W.index, df_Jal_W['Retail_and_Recreation'], label="Tiendas y Recreacion")
ax.plot(df_Jal_W.index, df_Jal_W['Grocery_and_Pharmacy'], label="Supermecado y farmacias")
ax.plot(df_Jal_W.index, df_Jal_W['Parks'], label="Parques")
ax.plot(df_Jal_W.index, df_Jal_W['Transit_Stations'], label="Estaciones de transito")
ax.plot(df_Jal_W.index, df_Jal_W['Workplaces'], label="Areas de trabajo")
ax.plot(df_Jal_W.index, df_Jal_W['Residences'], label="Residencias")
ax.set_ylabel("Movilidad")
ax.set_xlabel("Tiempo")
ax.set_title("Movilidad en Jalisco 2020")
plt.xticks(rotation='vertical')
ax.legend(loc="center left", bbox_to_anchor=(1,0)) 
#plt.tight_layout()
plt.show()

        



#####################################




