# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import pandas as pd
import matplotlib.pyplot as plt
datos=pd.read_csv('Desocupacion.csv',header=0)
print(datos)
newJalisco = (datos['Jalisco'])
indices_2019 = (newJalisco.loc[7:10])
print(indices_2019)
indices_2020 = (newJalisco.loc[11:14])
print(indices_2020)
#Promedio, desviacion estandar, maximo y minimo.
#indices_2019.describe()
#indices_2020.describe()

newJalisco["Jalisco"].plot()
plt.show()

