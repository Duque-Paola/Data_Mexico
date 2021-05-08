import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import pathlib
import os

def return_df():
    URL="https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
    #df=pd.read_csv(URL, low_memory=False) 
    df=pd.read_csv(URL, low_memory=False)
    
    
    df=df[df.country_region_code=='MX']
    df['date'] =  pd.to_datetime(df['date'])
    #df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
    df['sub_region_1'].fillna(value=0)
    df.drop('sub_region_2',1,inplace=True)
    df.rename(columns={'sub_region_1': 'State',
                       'retail_and_recreation_percent_change_from_baseline': 'Retail_and_Recreation', 
                       'grocery_and_pharmacy_percent_change_from_baseline':'Grocery_and_Pharmacy', 
                       'parks_percent_change_from_baseline':'Parks',
                       'transit_stations_percent_change_from_baseline': 'Transit_Stations',
                       'workplaces_percent_change_from_baseline':'Workplaces',
                       'residential_percent_change_from_baseline': 'Residences',
                       'date':'Date'},inplace=True)
    df=df[['Date',
           'State',
           #'Retail_and_Recreation',
           #'Grocery_and_Pharmacy',
           #'Parks',
           #'Transit_Stations',
           #'Workplaces',
           'Residences']]
    #define rango de fechas
    df = df.loc[(df['Date'] > '2020-02-15') & (df['Date'] < '2021-04-01')]
    return df

if __name__ == '__main__':
    df = return_df()
    path = pathlib.Path(__file__).parent.absolute()
    os.chdir(path)
    df.to_csv("data/google_movilidad_marzo_2021.csv")