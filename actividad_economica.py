#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:06:34 2020

@author: nacho
"""
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
from matplotlib import pyplot as plt
sns.set(color_codes=True)
import os, datetime
from collections import Counter
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker as ticker
#%%
path = "/home/nacho/Documents/coronavirus/Data_Mexico"
os.chdir(os.path.join(path)) 
act_econ_og = pd.read_csv("data/Actividad_Economica_Estatal.csv", encoding='utf-8')
#%%ACT ECON Mexico
act_econ_mx_2020 = act_econ_og.loc[2,['Unnamed: 83','Unnamed: 84','2020','Unnamed: 87']]
act_econ_mx_2020.index =  ['t3','t4','t1','t2']

act_econ_mx_2019 = act_econ_og.loc[2,['Unnamed: 78','Unnamed: 79','2019','Unnamed: 82']]
act_econ_mx_2019.index =  ['t3','t4','t1','t2']

#plot
fig, ax = plt.subplots()
ax.plot(act_econ_mx_2020.index, act_econ_mx_2020, label="2019-2020")
ax.plot(act_econ_mx_2019.index, act_econ_mx_2019, label="2018-2019")
ax.set_ylabel("Índice de volumen físico ")
ax.set_xlabel("Trimestres")
ax.set_title("Actividad Economica en México")
plt.xticks(rotation='vertical')
ax.legend()

#porcentaje
print("Total Mexico 2020: ", act_econ_mx_2020.astype(float).sum())
print("Total Mexico 2019: ", act_econ_mx_2019.astype(float).sum())
print("Porcentaje de incremento de Mexico:", act_econ_mx_2020.astype(float).sum()/act_econ_mx_2019.astype(float).sum()*100-100)
#%%ACT ECON JALISCO
act_econ_jal_2020 = act_econ_og.loc[16,['Unnamed: 83','Unnamed: 84','2020','Unnamed: 87']]
act_econ_jal_2020.index =  ['t3','t4','t1','t2']

act_econ_jal_2019 = act_econ_og.loc[16,['Unnamed: 78','Unnamed: 79','2019','Unnamed: 82']]
act_econ_jal_2019.index =  ['t3','t4','t1','t2']

#plot
fig, ax = plt.subplots()
ax.plot(act_econ_jal_2020.index, act_econ_jal_2020, label="2019-2020")
ax.plot(act_econ_jal_2019.index, act_econ_jal_2019, label="2018-2019")
ax.set_ylabel("Índice de volumen físico ")
ax.set_xlabel("Trimestres")
ax.set_title("Actividad Economica en Jalisco")
plt.xticks(rotation='vertical')
ax.legend()

#porcentaje
print("Total Jalisco 2020: ", act_econ_jal_2020.astype(float).sum())
print("Total Jalisco 2019: ", act_econ_jal_2019.astype(float).sum())
print("Porcentaje de incremento de Jalisco:", act_econ_jal_2020.astype(float).sum()/act_econ_jal_2019.astype(float).sum()*100-100)