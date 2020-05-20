import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 100)

da = pd.read_csv("nhanes_2015_2016.csv")
'''
Bivariate data arise when every "unit of analysis" (e.g. a person in the NHANES dataset) is assessed with respect to two traits 
(the NHANES subjects were assessed for many more than two traits, but we can consider two traits at a time here).

A scatterplot is a very common and easily-understood visualization of quantitative bivariate data. Below we make a scatterplot 
of arm length against leg length. This means that arm length (BMXARML) is plotted on the vertical axis and leg length (BMXLEG) 
is plotted on the horizontal axis). We see a positive dependence between the two measures -- people with longer arms tend 
to have longer legs, and vice-versa. However it is far from a perfect relationship.

In a scatterplot with more than around 100 points, "overplotting" becomes an issue. This means that many points fall on top 
of each other in the plot, which obscures relationships in the middle of the distribution and over-emphasizes the extremes. 
One way to mitigate overplotting is to use an "alpha" channel to make the points semi-transparent, as we have done below.
'''
sns.regplot(x="BMXLEG", y="BMXARML", data=da, fit_reg=False, scatter_kws={"alpha": 0.2})
# plt.show()

'''
Another way to avoid overplotting is to make a plot of the "density" of points. In the plots below, darker colors indicate where
 a greater number of points fall. The two plot margins show the densities for the arm lengths and leg lengths separately, while 
 the plot in the center shows their density jointly.

This plot also shows the Pearson correlation coefficient between the arm length and leg length, which is 0.62. As discussed in 
the course, the Pearson correlation coefficient ranges from -1 to 1, with values approaching 1 indicating a more perfect positive 
dependence. In many settings, a correlation of 0.62 would be considered a moderately strong positive dependence.
'''
sns.jointplot(x="BMXLEG", y="BMXARML", kind='kde', data=da)
# plt.show()

'''
As another example with slightly different behavior, we see that systolic and diastolic blood pressure (essentially the maximum
 and minimum blood pressure between two consecutive heart beats) are more weakly correlated than arm and leg length, with a
  correlation coefficient of 0.32. This weaker correlation indicates that some people have unusually high systolic blood pressure
   but have average diastolic blood pressure, and vice versa.
'''
sns.jointplot(x="BPXSY1", y="BPXDI1", kind='kde', data=da)
# plt.show()

'''
Next we look at two repeated measures of systolic blood pressure, taken a few minutes apart on the same person. These values are 
very highly correlated, with a correlation coefficient of around 0.96.
'''
jp = sns.jointplot(x="BPXSY1", y="BPXSY2", kind='kde', data=da)
# plt.show()

'''
Heterogeneity and stratification
Most human characteristics are complex -- they vary by gender, age, ethnicity, and other factors. This type of variation is often 
referred to as "heterogeneity". When such heterogeneity is present, it is usually productive to explore the data more deeply by 
stratifying on relevant factors, as we did in the univariate analyses.

Below, we continue to probe the relationship between leg length and arm length, stratifying first by gender, then by gender and 
ethnicity. The gender-stratified plot indicates that men tend to have somewhat longer arms and legs than women -- this is reflected 
in the fact that the cloud of points on the left is shifted slightly up and to the right relative to the cloud of points on the right.
 In addition, the correlation between arm length and leg length appears to be somewhat weaker in women than in men.
'''
da["RIAGENDRx"] = da.RIAGENDR.replace({1: "Male", 2: "Female"})
sns.FacetGrid(da, col="RIAGENDRx").map(plt.scatter, "BMXLEG", "BMXARML", alpha=0.4).add_legend()
# plt.show()

'''
Consistent with the scatterplot, a slightly weaker correlation between arm length and leg length in women (compared to men) can be 
seen by calculating the correlation coefficient separately within each gender.

The 'corr' method of a dataframe calculates the correlation coefficients for every pair of variables in the dataframe. 
This method returns a "correlation matrix", which is a table containing the correlations between every pair of variables in 
the data set. Note that the diagonal of a correlation matrix always contains 1's, since a variable always has correlation 1 
with itself. The correlation matrix is also symmetric around this diagonal, since the correlation between two variables 
'X' and 'Y' does not depend on the order in which we consider the two variables.

In the results below, we see that the correlation between leg length and arm length in men is 0.50, while in women the 
correlation is 0.43.
'''
print(da.loc[da.RIAGENDRx=="Female", ["BMXLEG", "BMXARML"]].dropna().corr())
print(da.loc[da.RIAGENDRx=="Male", ["BMXLEG", "BMXARML"]].dropna().corr())

'''
Next we look to stratifying the data by both gender and ethnicity.  This results in 2 x 5 = 10 total strata, since there are 
2 gender strata and 5 ethnicity strata. These scatterplots reveal differences in the means as well a diffrences in the degree
 of association (correlation) between different pairs of variables.  We see that although some ethnic groups tend to have 
 longer/shorter arms and legs than others, the relationship between arm length and leg length within genders is roughly 
 similar across the ethnic groups.  

One notable observation is that ethnic group 5, which consists of people who report being multi-racial or are of any race 
not treated as a separate group (due to small sample size), the correlation between arm length and leg length is stronger, 
especially for men.  This is not surprising, as greater heterogeneity can allow correlations to emerge that are indiscernible 
in more homogeneous data. 
'''
_ = sns.FacetGrid(da, col="RIDRETH1",  row="RIAGENDRx").map(plt.scatter, "BMXLEG", "BMXARML", alpha=0.5).add_legend()
# plt.show()

'''
Categorical bivariate data
In this section we discuss some methods for working with bivariate data that are categorical. We can start with a contingency 
table, which counts the number of people having each combination of two factors. To illustrate, we will consider the NHANES
 variables for marital status and education level.

First, we create new versions of these two variables using text labels instead of numbers to represent the categories. We also
 create a new data set that omits people who responded "Don't know" or who refused to answer these questions.
'''
da["DMDEDUC2x"] = da.DMDEDUC2.replace({1: "<9", 2: "9-11", 3: "HS/GED", 4: "Some college/AA", 5: "College",
                                       7: "Refused", 9: "Don't know"})
da["DMDMARTLx"] = da.DMDMARTL.replace({1: "Married", 2: "Widowed", 3: "Divorced", 4: "Separated", 5: "Never married",
                                      6: "Living w/partner", 77: "Refused"})
db = da.loc[(da.DMDEDUC2x != "Don't know") & (da.DMDMARTLx != "Refused"), :]

'''
Now we can create a contingency table, counting the number of people in each cell defined by a combination of education 
and marital status.
'''
x = pd.crosstab(db.DMDEDUC2x, da.DMDMARTLx)
print("\n", x)
print("\n")
db.groupby(["RIAGENDRx", "DMDEDUC2x", "DMDMARTLx"]).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)

'''
One factor behind the greater number of women who are divorced and widowed could be that women live longer than men. 
To minimize the impact of this factor, we can recalculate the above table using a few narrow bands of ages. To simplify 
here, we collapse the marital status data to characterize people as being either "married" or "unmarried" This allows 
us to focus on the marriage rate, which is a widely-studied variable in social science research.

There are a number of intriguing results here. For example, the marriage rate seems to drop as college-educated people 
get older (e.g. 71% of college educated women between 49 and 50 are married, but only 65% of college educated women 
between 50 and 59 are married, an even larger drop occurs for men). However in people with a HS/GED level of education, 
the marriage rate is higher for older people (although it is lower compared to the college educated sample). There are 
a number of possible explanations for this, for example, that remarriage after divorce is less common among college 
graduates.
'''
print('\n')
dx = db.loc[(db.RIDAGEYR >= 40) & (db.RIDAGEYR < 50)]
a = dx.groupby(["RIAGENDRx", "DMDEDUC2x", "DMDMARTLx"]).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)

dx = db.loc[(db.RIDAGEYR >= 50) & (db.RIDAGEYR < 60)]
b = dx.groupby(["RIAGENDRx", "DMDEDUC2x", "DMDMARTLx"]).size().unstack().fillna(0).apply(lambda x: x/x.sum(), axis=1)

print(a.loc[:, ["Married"]].unstack())
print("")
print(b.loc[:, ["Married"]].unstack())


'''
When we have enough data, a "violinplot" gives a bit more insight into the shapes of the distributions compared to a 
traditional boxplot. The violinplot below is based on the same data as the boxplot above. We can see quite clearly that 
the distributions with low mean (living with partner, never married) are strongly right-skewed, while the distribution 
with high mean (widowed) is strongly left-skewed. The other distributions have intermediate mean values, and are 
approximately symmetrically distributed. Note also that the never-married distribution has a long shoulder, suggesting 
that this distributions includes many people who are never-married because they are young, and have not yet reached the 
ages when people typically marry, but also a substantial number of people will marry for the first time anywhere from 
their late 30's to their mid-60's.
'''

plt.figure(figsize=(12, 4))
a = sns.violinplot(da.DMDMARTLx, da.RIDAGEYR)
plt.show()