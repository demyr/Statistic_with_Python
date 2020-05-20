import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib as plt
pd.set_option('display.max_columns', 100) # Show all columns when looking at dataframe

# Download NHANES 2015-2016 data
df = pd.read_csv("nhanes_2015_2016.csv")
df.index = range(1,df.shape[0]+1)
print(df.head())

# # One possible way of doing this is:
# pd.Series.mean(df[df.RIDAGEYR > 60].loc[range(0,100), 'BPXSY1'])
# # Current version of python will include this warning, older versions will not

# test our code on only ten rows so we can easily check
test = pd.DataFrame({'col1': np.repeat([3,1],5), 'col2': range(3,13)}, index=range(1,11))
print(test)

print(pd.Series.mean(test[test.col1 > 2].loc[0:5, 'col2']))