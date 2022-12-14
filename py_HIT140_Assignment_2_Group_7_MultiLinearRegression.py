import pandas as pd
import math
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error


#https://github.com/Gaelim/youtube/blob/master/Outliers.ipynb
def traditional_outlier(df,x):
    q1  =  df[x].quantile(.25)
    q3  =  df[x].quantile(.75)
    iqr = q3-q1
    df['Traditional']  = np.where(df[[x]]<(q1-1.5*iqr),-1,
                         np.where(df[[x]]>(q3+1.5*iqr),-1,1))
    return df

def outliers_find(df,x):
    df['Local Outlier'] = LocalOutlierFactor(n_neighbors=5, novelty=True).fit(df[[x]]).predict(df[[x]])
    df['Isolation Forest'] = IsolationForest().fit(df[[x]]).predict(df[[x]])
    df['Elliptical'] = EllipticEnvelope().fit(df[[x]]).predict(df[[x]])
    return df

def outliers_find(df,x):
    q1  =  df[x].quantile(.25)
    q3  =  df[x].quantile(.75)
    iqr = q3-q1
    df['Traditional']  = np.where(df[[x]]<(q1-1.5*iqr),-1,
                         np.where(df[[x]]>(q3+1.5*iqr),-1,1))
    df['Local Outlier'] = LocalOutlierFactor(n_neighbors=5, novelty=True).fit(df[[x]]).predict(df[[x]])
    df['Isolation Forest'] = IsolationForest().fit(df[[x]]).predict(df[[x]])
    df['Eliptic Envelope'] =EllipticEnvelope().fit(df[[x]]).predict(df[[x]])
    return df

def multicollinearity_check(X, thresh=5.0):
    data_type = X.dtypes
    # print(type(data_type))
    int_cols = \
    X.select_dtypes(include=['int', 'int16', 'int32', 'int64', 'float', 'float16', 'float32', 'float64']).shape[1]
    total_cols = X.shape[1]
    try:
        if int_cols != total_cols:
            raise Exception('All the columns should be integer or float, for multicollinearity test.')
        else:
            variables = list(range(X.shape[1]))
            dropped = True
            print('''\n\nThe VIF calculator will now iterate through the features and calculate their respective values.
            It shall continue dropping the highest VIF features until all the features have VIF less than the threshold of 5.\n\n''')
            while dropped:
                dropped = False
                vif = [variance_inflation_factor(X.iloc[:, variables].values, ix) for ix in variables]
                print('\n\nvif is: ', vif)
                maxloc = vif.index(max(vif))
                if max(vif) > thresh:
                    print('dropping \'' + X.iloc[:, variables].columns[maxloc] + '\' at index: ' + str(maxloc))
                    # del variables[maxloc]
                    X.drop(X.columns[variables[maxloc]], 1, inplace=True)
                    variables = list(range(X.shape[1]))
                    dropped = True

            print('\n\nRemaining variables:\n')
            print(X.columns[variables])
            # return X.iloc[:,variables]
            return X
    except Exception as e:
        print('Error caught: ', e)

#outliers
from sklearn.neighbors   import LocalOutlierFactor
from sklearn.covariance  import EllipticEnvelope
from sklearn.ensemble    import IsolationForest

# Read dataset into a DataFrame
df1 = pd.DataFrame()
dfOutliers1           =  pd.DataFrame()
dfUutliers2           =  pd.DataFrame()
dfTtraditional_outlier=  pd.DataFrame()

df = pd.read_csv(r"C:\temp\FairFieldAssTwoData_Ver7.csv")
#could not get the whole Dataframe clean function  to work!!!

##REMOVE NULLS
##PER COLUMN solution works better than a whole DATAFRAME null removal!
df['Elevation'].fillna(      int(df['Elevation'].mean()), inplace=True)
df['Drainage Area'].fillna(  int(df['Drainage Area'].mean()), inplace=True)
df['Surface Area'].fillna(   int(df['Surface Area'].mean()), inplace=True)
df['Max Depth'].fillna(      int(df['Max Depth'].mean()), inplace=True)
df['RF'].fillna(  int(df['RF'].mean()), inplace=True)
df['FR'].fillna(  int(df['FR'].mean()), inplace=True)
df['Dam'].fillna( int(df['Dam'].mean()), inplace=True)
df['RT'].fillna(  int(df['RT'].mean()), inplace=True)
df['RS'].fillna(  int(df['RS'].mean()), inplace=True)

# mean imputation
#df.fillna(df.mean(), inplace=True)
#DELETE A ROW OF NULLS/NANS"
df.drop(df.tail(1).index,inplace=True) # Delete Last Row Which is made up of nulls and zeros

#SHOW ME THE RESULTS!
#print(df.to_string())
#DO A multicolinearity check on the data set!
print(multicollinearity_check(df,5.0))

####NEW CODE

#look for outliers
dfOutliers1           = outliers_find(df,'Mercury')
dfUutliers2           = outliers_find(df,'Mercury')
dfTtraditional_outlier= traditional_outlier(df,'Mercury')

#drop the extra columns the OUTLIER checks added to the dataframe
df = df.drop(['Eliptic Envelope','Isolation Forest','Local Outlier','Traditional'], axis=1, errors='ignore')
#drop the clusters for the HEATMAP dataframe which will be used for the Heatmap graph
heatmapDF=  df.drop(['C1','C2','C3','C4','C5','C6'], axis=1, errors='ignore')

##This section generates the OUTLIER GRAPHS Which oddly open in a web browser!
fig1=px.box(data_frame=dfOutliers1,x='Local Outlier')
fig2=px.box(data_frame=dfUutliers2,x='Isolation Forest')
fig3=px.box(data_frame=dfTtraditional_outlier,x='Eliptic Envelope')
fig4=px.violin(data_frame=dfOutliers1,x='Local Outlier')
fig5=px.violin(data_frame=dfUutliers2,x='Isolation Forest')
fig6=px.violin(data_frame=dfTtraditional_outlier,x='Eliptic Envelope')
fig7=px.box(data_frame=df,x='Mercury')
fig1.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()
fig6.show()
fig7.show()
plt.show()
###

###DUE TO THE OUTLIERS in the MERCURY
#i removed the following 4 rows
#Reservoir	   Fish	Mercury	Elevation	Drainage Area	Surface Area	Max Depth	RF	FR	Dam	RT	RS	C1	C2	C3	C4	C5	C6
#Parker Lake	4	2.5	        50	1	35	22	0.63	3.9	1	2	1	1	0	0	0	0	0
#Fox Creek   	6	1.8	       1154	19	201	42	0.62	0.9	NA	1	1	0	1	0	0	0	0
#Two Dam Creek	3	1.25	306	14	290	41	0.51	3.7	0	2	1	0	1	0	0	0	0
#Temple Creek	5	1.22	276	3	210	38	0.53	1.4	0	2	1	1	0	0	0	0	0

#I MANUALLY CHANGED THE RESOURVOUR NAMES TO SEQUENTIAL NUMBERS (1,2,3,4...etc)

#BUILD AND EVALUATE A LINEAR REGRESSION MODEL


#This builds the Correlation Heatmap
# Plot correlation matrix
corr = heatmapDF.corr()
# Plot the pairwise correlation as heatmap
# Increase the size of the heatmap.
plt.figure(figsize=(16, 6))
# Store heatmap object in a variable to easily access it when you want to include more features (such as title).
# Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
heatmap = sns.heatmap(heatmapDF.corr(), vmin=-1, vmax=1, annot=True)
# Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);
plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(heatmapDF.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12);
# save heatmap as .png file
# dpi - sets the resolution of the saved image in dots/inches
# bbox_inches - when set to 'tight' - does not allow the labels to be cropped
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

###
# create dummies for clusters
dum_clusters = pd.get_dummies(df[['C1','C2','C3','C4','C5','C6']])

# define Xs and Y for regression
X = pd.concat([df[['Elevation','Drainage Area','Surface Area','Max Depth',
                    'RF','FR','Dam','RT','RS']], dum_clusters], axis=1)
y = df['Mercury']

# fit model
regr = sm.OLS(y,X).fit()
print(regr.summary())

#Final Plots for report
# residual plots
fig = plt.figure(figsize=(12,8))
fig = sm.graphics.plot_regress_exog(regr, 'Elevation', fig=fig)
plt.show()
