# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import os
#%%
path = "/home/nacho/Documents/coronavirus/Data_Mexico"
os.chdir(os.path.join(path)) 
datos = pd.read_csv("data/Desocupacion.csv",header=0)
#datos=pd.read_csv('Desocupacion.csv',header=0)
print(datos)
#%%JALISCO
newJalisco = (datos['Jalisco'])
indices_2019 = newJalisco.loc[[7,8,9,11]]
print(indices_2019)
indices_2020 = (newJalisco.loc[[12,13,14,16]])
print(indices_2020)

index = ["T2","T3","T4","T1"]

indices_2019.index = index
indices_2020.index = index

#plot
fig, ax = subplots()
indices_2019.plot()
indices_2020.plot()
ax.legend(["2018-2019", "2019-2020"])
ax.set_title("Tasa de Desocupación en Jalisco")
plt.show()

#porcentaje
print("Total Jalisco 2020: ", indices_2020.astype(float).sum())
print("Total Jalisco 2019: ", indices_2019.astype(float).sum())
print("Porcentaje de incremento de Jalisco:", indices_2020.astype(float).sum()/indices_2019.astype(float).sum()*100-100)
#%%NACIONAL
datos_mx = pd.read_csv("data/desocupacion_nacional_oct_2020.csv",header=0)

datos_mx_2020 = datos_mx['“tasa_desocupacion”'].iloc[180:190,]

datos_mx_2019 = datos_mx['“tasa_desocupacion”'].iloc[168:178,]

index_month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre']

datos_mx_2020.index = index_month
datos_mx_2019.index = index_month

#plot
fig, ax = subplots()
datos_mx_2019.plot()
datos_mx_2020.plot()
ax.legend(["2019", "2020"])
ax.set_title("Tasa de Desocupación en Mexico")
plt.show()

#porcentaje
print("Total Mexico 2020: ", datos_mx_2020.astype(float).sum())
print("Total Mexico 2019: ", datos_mx_2019.astype(float).sum())
print("Porcentaje de incremento de Mexico:", datos_mx_2020.astype(float).sum()/datos_mx_2019.astype(float).sum()*100-100)
