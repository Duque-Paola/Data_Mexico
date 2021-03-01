#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:06:34 2020

@author: nacho

crear para todos los estados dataset con diccionario

"""
#%%
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
#%%
path = "/home/nacho/Documents/coronavirus/Data_Mexico"
os.chdir(os.path.join(path)) 
delitos_df = pd.read_csv("data/IDEFC_NM_dic2020.csv", encoding='latin-1',thousands=',')
movilidad = movilidad.return_df()
#%%
#delitos_df = delitos_df[delitos_df['Entidad'] == 'Tlaxcala']
#%%
states = delitos_df.Entidad.value_counts().index.tolist()
states.insert(0, None)
for state in states:
#%%
    if state is not None:
        delitos_df = delitos_df[delitos_df['Entidad'] == state]
    #delitos_df['Tipo de delito'].value_counts()
    delitos_list = delitos_df['Tipo de delito'].value_counts().index.tolist()
    delitos_sum_df = pd.DataFrame(index = pd.date_range('2015-01', '2021-01', freq='M'))
    #delitos_sum_df.index = delitos_sum_df.index.to_period('M')
    delitos_sum_df.index.name = 'date'
    years = np.arange(2015,2021)
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    for delito in delitos_list:
        values_delito = []
        for year in years:
            for mes in meses:
                value = delitos_df.loc[(delitos_df['Tipo de delito'] == delito) & (delitos_df['Año'] == year), mes].sum()
                values_delito.append(value)
        delitos_sum_df[str(delito)] = values_delito
#%%correlation
        movilidad_df = movilidad.loc[(movilidad['Province'] == state) & (movilidad['Date'] > '2020-02-15') & (movilidad['Date'] < '2021-01-01')]
        movilidad_df = movilidad_df['Residences'].resample('M').sum()
        delitos_corr_df = delitos_sum_df.loc['2020-02':]
        stats.pearsonr(movilidad_df, delitos_corr_df['Feminicidio'])[0]
#%%stat analysis
decomposition = sm.tsa.seasonal_decompose(delitos_sum_df['Feminicidio'], model='additive')
fig = decomposition.plot()
matplotlib.rcParams['figure.figsize'] = [9.0, 5.0] 
#%%plot
delitos_sum_df.plot(linewidth=2, fontsize=12).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))

fig, axes = plt.subplots(nrows=2, ncols=1, squeeze=False)
delitos_sum_df['Robo'].plot(ax=axes[0,0], legend=True)
delitos_sum_df['Abuso sexual'].plot(ax=axes[1,0], legend=True)
plt.tight_layout()
plt.show();
#%%training
delitos_pred = delitos_sum_df.copy()
delitos_pred['Year'] = pd.date_range('2015-01', '2021-01', freq='M')
series = TimeSeries.from_dataframe(delitos_pred, 'Year',['Allanamiento de morada'])
series.plot()

train, val = series.split_before(pd.Timestamp('20200301'))
train.plot(label='training')
val.plot(label='validation')
plt.legend();
#%%
def best_k(train):
    #plot_acf(train, m = 12, alpha = .05)
    for m in range(2, 25):
        is_seasonal, period = check_seasonality(train, m=m, alpha=.05)
        if is_seasonal:
            final_k = period
            print('There is seasonality of order {}.'.format(period))
            return final_k
        if not is_seasonal:
            return 12

def best_theta(val, train):
    thetas = 2 - np.linspace(-10, 10, 50)
    best_mape = float('inf')
    best_theta = 0
    for theta in thetas:
        model = Theta(theta)
        model.fit(train)
        pred_theta = model.predict(len(val))
        res = mape(val, pred_theta)
        if res < best_mape:
            best_mape = res
            best_theta = theta
    return best_theta

def best_fft(val, train):
    freqs = np.arange(2,31)
    best_mape = float('inf')
    best_freq = 0
    for freq in freqs:
        model = FFT(nr_freqs_to_keep= freq)
        model.fit(train)
        pred_freq = model.predict(len(val))
        res = mape(val, pred_freq)
        if res < best_mape:
            best_mape = res
            best_freq = freq
    return best_freq
#%%
final_k = best_k(train)
best_theta = best_theta(val, train)
best_freq = best_fft(val, train)

'''
models = [
    NaiveSeasonal(),
    NaiveSeasonal(K=final_k),
    NaiveDrift(),
    Prophet(),
    ExponentialSmoothing(),
    ARIMA(),
    AutoARIMA(),
    Theta(best_theta),
    Theta(),
    FFT(),
    FFT(trend='poly'),
    FFT(trend='exp'),
    FFT(nr_freqs_to_keep=best_freq)]
'''
models = [ExponentialSmoothing(), Prophet()]

best_mape = float('inf')

for i, model in enumerate(models):
    model.fit(train)
    prediction = model.predict(len(val))
    #series.plot(label='actual')
    #prediction.plot(label='forecast', lw=2)
    #plt.legend()
    res = MASE(training_series=train, testing_series= val, prediction_series = prediction)
    print(str(model),': ',res)
    if res < best_mape:
        best_mape = res
        best_model = model
        best_prediction = prediction


train.plot(label='train')
val.plot(label='true')
best_prediction.plot(label='prediction')
plt.legend();
print(best_mape,
      best_model,
      best_prediction)

val.sum()[0]
best_prediction.sum()[0]

#%%