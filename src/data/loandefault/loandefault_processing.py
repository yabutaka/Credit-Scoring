import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder

#List to get all columns filled with NaNs to drop
nan_filled_cols = ['TARGET']
#Load in the dataset 
apps = pd.read_csv("./application_data.csv")
apps_types = apps
#Clean columns 'OCCUPATION_TYPE','OWN_CAR_AGE', 'DAYS_BIRTH', and create column 'outcome'
apps['OCCUPATION_TYPE'] = apps['OCCUPATION_TYPE'].fillna("Unemployed")
apps['OWN_CAR_AGE'] = apps['OWN_CAR_AGE'].fillna(200)
apps['DAYS_BIRTH'] = apps[['DAYS_BIRTH']].apply(lambda x: abs(x) // 365)
apps['outcome'] = apps['TARGET']
for col in apps.columns:
    tot = len(apps[col])
    nans_tot = apps[col].isna().sum()
    #Get percentage of each column that is NaN
    perc = nans_tot / tot 
    #Fill NaNs with 0 for time being
    if apps[col].dtypes == "O":
        apps[col] =  apps[col].fillna("")
    elif  apps[col].dtypes != "O":
        apps[col] =  apps[col].fillna(0)
    #If NaNs are more than 15% of column drop the column 
    if perc > 0.15:
        nan_filled_cols.append(col)
#drop all NaN columns and TARGET
apps = apps.drop(columns = nan_filled_cols)
 
#OrdinalEncode object columns 
for col in apps.columns:
    oe = OrdinalEncoder()
    if apps[col].dtypes == "O":
        apps[col] =  oe.fit_transform(apps[[col]].to_numpy().reshape(-1,1))
        apps[col] = apps[col].apply(lambda x: int(round(x)))

#Get type information and summary
types = [str(kind) for kind in apps.dtypes.to_numpy()]
di = {"Columns": list(apps.columns), "Dtypes" : types }
di = pd.DataFrame(apps)

#Save data as CSV file
apps.to_csv("src/data/loandefault/loandefault_data.csv", index= False)
di.to_csv("src/data/loandefault/loandefault_info.csv", index = False)

