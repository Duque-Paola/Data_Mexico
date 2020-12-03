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
violencia_og = pd.read_csv("data/IDEFC_NM_oct2020.csv", encoding='utf-8')