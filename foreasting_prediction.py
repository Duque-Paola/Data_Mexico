#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:06:34 2020

@author: nacho

crear para todos los estados dataset con diccionario

"""
#%%
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns; sns.set()
from scipy import stats
from matplotlib import pyplot as plt
sns.set(color_codes=True)
import os, datetime
from collections import Counter
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker as ticker
from darts import TimeSeries
from darts.metrics import mape, mase
from darts.utils.statistics import check_seasonality, plot_acf, plot_residuals_analysis
from darts.models import (
    NaiveSeasonal,
    NaiveDrift,
    Prophet,
    ExponentialSmoothing,
    ARIMA,
    AutoARIMA,
    StandardRegressionModel,
    Theta,
    FFT
)
import warnings
warnings.filterwarnings("ignore")
import logging
logging.disable(logging.CRITICAL)
import movilidad
import statsmodels.api as sm
from itertools import product
import math
from sklearn.preprocessing import MinMaxScaler
matplotlib.rcParams['figure.figsize'] = [9.0, 5.0]
#%%
path = "/home/nacho/Documents/coronavirus/Data_Mexico"
os.chdir(os.path.join(path)) 
delitos_df = pd.read_csv("data/IDEFC_NM_dic2020.csv", encoding='latin-1',thousands=',')
#delitos_df = pd.read_csv("data/IDEFC_NM_mar2021.csv", encoding='latin-1',thousands=',')
#movilidad = movilidad.return_df()
df_movilidad = pd.read_csv("data/google_movilidad.csv", index_col='Date')
#%%
########################
#########ESTADOS########
########################
#%%hacer listas de valores unicos 
dict_delitos_sum = {}
states = delitos_df.Entidad.value_counts().index.tolist()
delitos_list = delitos_df['Tipo de delito'].value_counts().index.tolist()

#%%Generar dict de delitos por estado 
for state in states:
    delitos_state = delitos_df[delitos_df['Entidad'] == state]
    delitos_sum_df = pd.DataFrame(index = pd.date_range('2015-01', '2021-01', freq='M'))
    #delitos_sum_df = pd.DataFrame(index = pd.date_range('2015-01', '2021-04', freq='M'))
    delitos_sum_df.index.name = 'date'
    years = np.arange(2015,2021)
    #years = np.arange(2015,2022)
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    for delito in delitos_list:
        values_delito = []
        for year in years:
            for mes in meses:
                value = delitos_state.loc[(delitos_state['Tipo de delito'] == delito) & (delitos_state['Año'] == year), mes].sum()
                values_delito.append(value)
        delitos_sum_df[str(delito)] = values_delito
        dict_delitos_sum[state] = delitos_sum_df
#%%generar dict con todas las comb de estados y delitos para guardar corr y trend
df_dsct = pd.DataFrame(list(product(states, delitos_list)), columns=['state', 'delito'])
df_dsct['corr'] = ""
df_dsct['trend'] = ""
#%%Generar df por delito por estado y su porcentaje de crecimento respecto al año pasado
for state in states:
    for delito in delitos_list:
        df_delito_state = dict_delitos_sum[state].sort_values(['date'])[delito]
        trend = df_delito_state.resample('Y').sum().pct_change()[-1]
        if np.isinf(trend):
            trend = math.inf
        df_dsct.loc[(df_dsct['state'] == state) & (df_dsct['delito'] == delito), ['trend']] = trend
#%%corr con moviliad
df_corr_movilidad = df_movilidad[df_movilidad['State'].notna()]

df_corr_movilidad['State'].replace({
    'Nuevo Leon': 'Nuevo León',
    'Mexico City': 'Ciudad de México', 
    'Yucatan':'Yucatán', 
    'Veracruz':'Veracruz de Ignacio de la Llave',
    'San Luis Potosi': 'San Luis Potosí',
    'workplaces_percent_change_from_baseline':'Querétaro',
    'Michoacán': 'Michoacán de Ocampo',
    'State of Mexico':'México',
    'Coahuila': 'Coahuila de Zaragoza'
    },inplace=True)

for state in states:
    for delito in delitos_list:
        df_delito_state = dict_delitos_sum[state].sort_values(['date'])[delito]
        movilidad_spec = df_corr_movilidad.loc[(df_corr_movilidad['State'] == state) & (df_corr_movilidad.index > '2020-02-15') & (df_corr_movilidad.index < '2021-01-01')]
        movilidad_spec.index = pd.to_datetime(movilidad_spec.index)
        movilidad_spec = movilidad_spec['Residences'].resample('M').sum()
        df_delito_state = df_delito_state.loc['2020-02':]
        corr = stats.pearsonr(movilidad_spec, df_delito_state)[0]
        df_dsct.loc[(df_dsct['state'] == state) & (df_dsct['delito'] == delito), ['corr']] = corr

#%%Limpiar df
df_dsct.drop(df_dsct[df_dsct['trend'] == "inf"].index, inplace = True)
df_dsct.drop(df_dsct[df_dsct['trend'] == "nan"].index, inplace = True)
df_dsct.drop(df_dsct[df_dsct['corr'] == "inf"].index, inplace = True)
df_dsct.drop(df_dsct[df_dsct['corr'] == "nan"].index, inplace = True)
df_dsct = df_dsct[pd.notnull(df_dsct['trend'])]
df_dsct = df_dsct[pd.notnull(df_dsct['corr'])]

#drop index
df_dsct = df_dsct.sort_values(by=['corr'],ignore_index=True, ascending = False)
#%%specific scaler
def spec_scaler(series, minv, maxv):
    series = series.values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(minv, maxv))
    scaler = scaler.fit(series)
    normalized_series = scaler.transform(series)
    return normalized_series
#%%prediction
def predict_series(df_delito_state, delito):
    df_pred = df_delito_state.copy()
    df_pred = pd.DataFrame(df_pred)
    
    df_pred['Year'] = pd.date_range('2015-01', '2021-01', freq='M')
    series = TimeSeries.from_dataframe(df_pred, 'Year', delito)
    #train, val = series.split_before(pd.Timestamp('20200201'))
    train, val = series.split_before(pd.Timestamp('20191230'))

    model = Prophet()
    #model = ExponentialSmoothing()
    model.fit(train)
    prediction = model.predict(len(val))
    prediction = prediction.pd_dataframe()
    prediction[prediction < 0] = 0
    return prediction
#%%
#plot df_dsct
for index in [0,1,2,3,4,5,6,7,8,9,10,11,-1,-2,-3,-4,-5]:
    
    index_delito_state = df_dsct.iloc[index,:]
    state = index_delito_state.loc['state']
    delito = index_delito_state.loc['delito']
    df_delito_state = dict_delitos_sum[state][delito]
    
    decom = sm.tsa.seasonal_decompose(df_delito_state, model = 'additive')
    
    movilidad_spec = df_corr_movilidad.loc[(df_corr_movilidad['State'] == state) & (df_corr_movilidad.index < '2021-01-01')]
    movilidad_spec.index = pd.to_datetime(movilidad_spec.index)
    movilidad_spec = movilidad_spec['Residences'].resample('M').sum()
    #plot
    fig, ax = plt.subplots() 
    ax.plot(movilidad_spec.index, spec_scaler(series = movilidad_spec, 
                                              minv = df_delito_state.loc[df_delito_state.index > '2020-02-15'].resample('M').sum().min(),
                                              maxv = df_delito_state.loc[df_delito_state.index > '2020-02-15'].resample('M').sum().max()),
            label = 'movilidad residencial **proporcional al delito',
            linestyle = ':',
            color = 'black',
            linewidth=2)
    ax.plot(decom.trend.index, decom.trend.values, label = 'Tendencia', linestyle='--', color='blue')
    ax.plot(decom.trend.index, df_delito_state.resample('M').sum(), label = 'Suma mensual del delito', color='red')
    ax.set_title(delito+' en '+state+
                 '\n'+'correlación del delito con movilidad: '+str(round(df_dsct.iloc[index,:]['corr'], 2))+
                 '\n'+'tendencia del delito respecto al año anterior: '+str(round(df_dsct.iloc[index,:]['trend'], 2)))
    df_pred = predict_series(df_delito_state, delito)
    ax.plot(df_pred.index,
            df_pred.values,
            label = 'predicción',
            color = 'green')
    
    ax.legend(loc='upper left')
    #plt.plot()
    fig.savefig('Plots/tendencias_delito_estado/'+state+str('_')+delito+'.png', format='png', dpi=800)