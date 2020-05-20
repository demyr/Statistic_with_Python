import numpy as np
import seaborn as sns
import pandas as pd

# Download NHANES 2015-2016 data
df = pd.read_csv("nhanes_2015_2016.csv")

# get columns names
col_names = df.columns
print(col_names)

# One way to get the column names we want to keep is simply by copying from the above output and storing in a list
keep = ['BMXWT', 'BMXHT', 'BMXBMI', 'BMXLEG', 'BMXARML', 'BMXARMC',
       'BMXWAIST']

# Another way to get only column names that include 'BMX' is with list comprehension
# [keep x for x in list if condition met]
keep = [column for column in col_names if 'BMX' in column]

# use [] notation to keep columns
df_BMX = df[keep]

index_bool = np.isin(df.columns, keep)
print(index_bool)

# Lets only look at rows who 'BMXWAIST' is larger than the median
waist_median = pd.Series.median(df_BMX['BMXWAIST']) # get the median of 'BMXWAIST'

# Lets add another condition, that 'BMXLEG' must be less than 32
condition1 = df_BMX['BMXWAIST'] > waist_median
condition2 = df_BMX['BMXLEG'] < 32
df_BMX[condition1 & condition2].head() # Using [] method
# Note: can't use 'and' instead of '&'

df_BMX.loc[condition1 & condition2, ['BMXBMI','BMXARML']].head() # Using df.loc[] method
# note that the conditiona are describing the rows to keep

# Lets make a small dataframe and give it a new index so can more clearly see the differences between .loc and .iloc
tmp = df_BMX.loc[condition1 & condition2, :].head()
tmp.index = ['a', 'b', 'c', 'd', 'e'] # If you use different years than 2015-2016, this my give an error. Why?
tmp

# We can use the .loc and .iloc methods to change values within the dataframe
tmp.iloc[0:3,2] = [0]*3
tmp.iloc[:,2]