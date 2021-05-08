#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:37:04 2021

@author: nacho
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
#import movilidad
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
#########NACIONAL########
########################
#%%hacer listas de valores unicos 
delitos_list = delitos_df['Tipo de delito'].value_counts().index.tolist()
#%%Generar dict de delitos

delitos_sum_df = pd.DataFrame(index = pd.date_range('2015-01', '2021-01', freq='M'))
delitos_sum_df.index.name = 'date'
years = np.arange(2015,2021)
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
#for i in range(len(delitos_sum_df)):
for index, row in delitos_sum_df.iterrows():
    for delito in delitos_list:
        values_delito = []
        for year in years:
            for mes in meses:
                value = delitos_df.loc[(delitos_df['Tipo de delito'] == delito) & (delitos_df['Año'] == year), mes].sum()
                values_delito.append(value)
        delitos_sum_df[delito] = values_delito
#%%generar df con cada delito con su corr y trend
df_dsct = pd.DataFrame(list(product(delitos_list)), columns=['delito'])
df_dsct['corr'] = ""
df_dsct['trend'] = ""
#%%Generar df por delito por estado y su porcentaje de crecimento respecto al año pasado
for delito in delitos_list:
    df_delito = delitos_sum_df[delito]
    trend = df_delito.resample('Y').sum().pct_change()[-1]
    if np.isinf(trend):
        trend = math.inf
    df_dsct.loc[df_dsct['delito'] == delito, ['trend']] = trend
#%%corr con movilidad
df_corr_movilidad = df_movilidad[df_movilidad['State'].isnull()]

for delito in delitos_list:
    df_delito = delitos_sum_df[delito]
    movilidad_spec = df_corr_movilidad.loc[(df_corr_movilidad.index > '2020-02-15') & (df_corr_movilidad.index < '2021-01-01')]
    movilidad_spec.index = pd.to_datetime(movilidad_spec.index)
    movilidad_spec = movilidad_spec['Residences'].resample('M').sum()
    df_delito = df_delito.loc['2020-02':]
    corr = stats.pearsonr(movilidad_spec, df_delito)[0]
    df_dsct.loc[df_dsct['delito'] == delito, ['corr']] = corr
#%%limpiar df
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
#%%plot df_dsct


for index in [0,1,2,-1,-2,-3,-4,-5]:
    
    index_delito_state = df_dsct.iloc[index,:]
    delito = index_delito_state.loc['delito']
    df_delito = delitos_sum_df[delito]
    
    decom = sm.tsa.seasonal_decompose(df_delito, model = 'additive')
    
    movilidad_spec = df_corr_movilidad.loc[df_corr_movilidad.index < '2021-01-01']
    movilidad_spec.index = pd.to_datetime(movilidad_spec.index)
    movilidad_spec = movilidad_spec['Residences'].resample('M').sum()
    #plot
    fig, ax = plt.subplots() 
    ax.plot(movilidad_spec.index, spec_scaler(series = movilidad_spec, 
                                              minv = df_delito.loc[df_delito.index > '2020-02-15'].resample('M').sum().min(),
                                              maxv = df_delito.loc[df_delito.index > '2020-02-15'].resample('M').sum().max()),
            label = 'movilidad residencial **proporcional al delito',
            linestyle = ':',
            color = 'black',
            linewidth=2)
    ax.plot(decom.trend.index, decom.trend.values, label = 'Tendencia', linestyle='--', color='blue')
    ax.plot(decom.trend.index, df_delito.resample('M').sum(), label = 'Suma mensual del delito', color='red')
    ax.set_title(delito+' en la República Mexicana '+
                 '\n'+'correlación del delito con movilidad: '+str(round(df_dsct.iloc[index,:]['corr'], 2))+
                 '\n'+'tendencia del delito respecto al año anterior: '+str(round(df_dsct.iloc[index,:]['trend'], 2)))
    df_pred = predict_series(df_delito, delito)
    ax.plot(df_pred.index,
            df_pred.values,
            label = 'predicción',
            color = 'green')
    
    ax.legend(loc='upper left')
    #plt.plot()
    fig.savefig('Plots/tendencias_delito_nacional/'+delito+'.png', format='png', dpi=800)








