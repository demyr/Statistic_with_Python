import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import numpy as np

pd.set_option('display.max_columns', None)

da = pd.read_csv("nhanes_2015_2016.csv")

'''
###
Relabel the marital status variable DMDMARTL to have brief but informative character labels.
Then construct a frequency table of these values for all people, then for women only, and for men only.
Then construct these three frequency tables using only people whose age is between 30 and 40.
'''

da["marital_status"] = da.DMDMARTL.replace({1: "Unmarried", 2: "Married", 3: "Widow", 4: "Divorced",
                                            5: "Separated", 6: "Registered partner", 7: "Separated partner"})
da["Education"] = da.DMDEDUC2.replace({1: "<9", 2: "9-11", 3: "HS/GED", 4: "Some college/AA", 5: "College",
                                       7: "Refused", 9: "Don't know"})

da["gender"] = da.RIAGENDR.replace({1: 'Male', 2: 'Female'})
da["agegrp"] = pd.cut(da.RIDAGEYR, [18, 30, 40, 50, 60, 70, 80])

da_male_all = da.loc[(da.gender == 'Male')]
da_female_all = da.loc[(da.gender == 'Female')]
da_male_30_40 = da.loc[(da.gender == 'Male') & da.RIDAGEYR.isin([30, 40])]
da_female_30_40 = da.loc[(da.gender == 'Female') & da.RIDAGEYR.isin([30, 40])]

print("All:")
print(da.marital_status.value_counts())

print("\n All Males")
print(da_male_all.marital_status.value_counts())

print("\n All Females")
print(da_female_all.marital_status.value_counts())

print("\n Males 30-40 year:")
print(da_male_30_40.marital_status.value_counts())

print("\n Females 30-40 year:")
print(da_female_30_40.marital_status.value_counts())

'''
###
Restricting to the female population, stratify the subjects into age bands no wider than ten years, 
and construct the distribution of marital status within each age band. 
Within each age band, present the distribution in terms of proportions that must sum to 1.
'''
print("\n Females marital status grouped by age:")
dx = da_female_all.loc[~da_female_all.DMDMARTL.isin(['77.0'])]
print(dx.groupby('agegrp').marital_status.value_counts().unstack().apply(lambda x: x / x.sum() * 100, axis=1).to_string(
    float_format="%.2f"))

'''
###
Repeat the construction for males.
'''
print("\n Males marital status grouped by age:")
dx = da_male_all.loc[~da_male_all.DMDMARTL.isin(['77.0'])]
print(dx.groupby('agegrp').marital_status.value_counts().unstack().apply(lambda x: x / x.sum() * 100, axis=1).to_string(
    float_format="%.2f"))

'''
###
Make a boxplot showing the distribution of within-subject differences between the first and second systolic blood pressure measurents 
(BPXSY1 and BPXSY2).
'''
sns.boxplot(da.BPXSY2 - da.BPXSY1)
plt.show()

'''
###
 Make side-by-side boxplots of the two systolic blood pressure variables.
'''
sns.boxplot(data=da.loc[:, ['BPXSY1', 'BPXSY2']]).set_ylim([120, 123])
plt.show()

'''
###
 Construct a frequency table of household sizes for people within each educational attainment category 
 (the relevant variable is DMDEDUC2). Convert the frequencies to proportions.
'''
print('frequency table of household sizes for people within each educational attainment category')

print(da.groupby('Education').DMDHHSIZ.value_counts().unstack().apply(lambda x: x / x.sum() * 100, axis=1).to_string(
    float_format="%.2f"))

'''
###
  Restrict the sample to people between 30 and 40 years of age. 
  Then calculate the median household size for women and men within each level of educational attainment.
'''

print('\n Female median')
print(da_female_30_40.groupby(['Education'])['DMDHHSIZ'].median())
print('\n Male median')
print(da_male_30_40.groupby(['Education'])['DMDHHSIZ'].median())

print('\n Show histogram of house hold size distribution for males in College educational attainment group')
male_30_40_college = da_male_30_40[da_male_30_40.Education == 'College']
print(male_30_40_college.shape)
sns.distplot(male_30_40_college.DMDHHSIZ, bins=6)
plt.show()
