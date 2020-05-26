
# import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# import statsmodels.api as sm
import numpy as np

da = pd.read_csv("../nhanes_2015_2016.csv")

'''
Question 1
Make a scatterplot showing the relationship between the first and second measurements of diastolic blood pressure 
(BPXDI1 and BPXDI2). Also obtain the 4x4 matrix of correlation coefficients among the first two systolic and the first 
two diastolic blood pressure measures.
'''
sns.regplot(x='BPXDI1', y='BPXDI2', data=da, fit_reg=False, scatter_kws={"alpha": 0.2})
print(da.loc[:, ['BPXSY1', 'BPXSY2']].dropna().corr())
print(da.loc[:, ['BPXSY1', 'BPXSY2', 'BPXDI1', 'BPXDI2']].dropna().corr())

'''
Question 2
Log transform the four blood pressure variables and repeat question 1.
'''
da['sys1log'] = np.log(da.BPXSY1.dropna())
da['sys2log'] = np.log(da.BPXSY2.dropna())
da['dis1log'] = np.log(da.BPXDI1.dropna())
da['dis2log'] = np.log(da.BPXDI2.dropna())
print(da.loc[:, ['sys1log', 'sys2log', 'dis1log', 'dis2log']].corr())